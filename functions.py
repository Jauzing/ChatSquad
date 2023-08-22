import tkinter as tk
import threading

background_color = "#509DCC"
text_color = "#FFFFFF"
font1 = "Cascadia Code"
font2 = "Cascadia Code"
titleFont = "Goudy Stout"
companyFont = "Harlow Solid Italic"

def show_splash_screen(root):# Show a welcome screen with instructions
    splash = tk.Toplevel(root)
    splash.geometry("1000x900")
    splash.configure(background=background_color)

    # Add title without figlet format, increase font size

    app_title = "\n ChatSquad"

    title_label = tk.Label(splash, text=app_title, bg=background_color, fg=text_color, font=(titleFont, 35))
    title_label.pack()

    # Add small text under title
    app_smalltext = "Thom & Deer"
    small_text = tk.Label(splash, text=app_smalltext, bg=background_color, fg=text_color, font=(companyFont, 18))
    small_text.pack()

    instructions = """
    - Choose a personality to chat with in the dropdown menu.

    - Write a message in the messagebox or hit "Start conversation" and the bot will initiate.

    - You can change personality any time.

    - The bot has some memory (close to a goldfish) and will remember what you previously talked about.

    - This memory is swiped when changing personality or exiting the program.

    - All your conversations are automatically saved in a file called "responses_personality.json".
    """

    instructions_label = tk.Label(splash, text=instructions, bg=background_color, fg=text_color)
    instructions_label.config(font=("Roboto", 14))
    instructions_label.pack()

    ok_button = tk.Button(splash, text="OK", command=lambda: [splash.destroy(), root.deiconify()])
    ok_button.config(font=("Roboto", 14))
    ok_button.config(bg=background_color)
    ok_button.config(fg=text_color)
    ok_button.pack()

    def start_chat(event=None):
        chosen_personality = personality_selection.get().strip()
        image = Image.open(f"imgs/{chosen_personality}.png")
        image.thumbnail((200, 200), Image.LANCZOS)
        profile_image = ImageTk.PhotoImage(image)
        image_label.configure(image=profile_image)
        image_label.image = profile_image
        print(f"Chosen personality: {chosen_personality}")

        user_message = user_input.get().strip()

        chat_area.configure(state='normal')
        chat_area.insert(tk.END, f"\n User: {user_message}\n")
        chat_area.configure(state='disabled')

        conversation_history.append({"role": "user", "content": user_message})

        messages = [
                       {"role": "system", "content": personalities[chosen_personality]},
                   ] + conversation_history

        print("Calling OpenAI API...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        print("User:" + user_message)
        print("\n")

        print(chosen_personality + " : " + response.choices[0].message["content"].strip())
        print("\n")

        response_text = response.choices[0].message["content"].strip()
        conversation_history.append({"role": "assistant", "content": response_text})

        chat_area.configure(state='normal')
        chat_area.insert(tk.END, f"\n {chosen_personality}: {response_text}\n")
        chat_area.configure(state='disabled')
        chat_area.yview(tk.END)

        user_input.delete(0, tk.END)

        print("Saving responses...")
        new_entry = {
            "prompt": response_text,
            "response": user_message
        }

        if os.path.exists('responses_personality.json'):
            with open('responses_personality.json', 'r', encoding='utf-8') as file:
                if os.stat('responses_personality.json').st_size == 0:
                    data = []
                else:
                    data = json.load(file)
            data.append(new_entry)
        else:
            data = [new_entry]

        with open('responses_personality.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("Saved ✔️")