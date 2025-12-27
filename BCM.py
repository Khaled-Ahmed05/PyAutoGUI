import pyautogui as pag
import pymsgbox as pmb
from pynput import keyboard
import time

program_running = True
paused = False
recipes = []
output_data = {}

def on_press(key):
    global paused
    if key == keyboard.Key.esc:
        paused = True
        return False  # stop listener ONLY

def capture_position(message, title):
    pmb.alert(
        text=message + "\n\nMove your mouse, then press Enter.",
        title="PyAutoGUI - " + title,
        button='OK'
    )
    return pag.position()

while program_running:
    toggle = pmb.confirm(
        text='Start the program?\nPress ESC to pause',
        title='PyAutoGUI',
        buttons=['OK', 'Cancel'] # type: ignore
    )

    if toggle == 'Cancel':
        program_running = False
        break

    if toggle == 'OK':
        # ===== SETUP PHASE =====
        recipes.clear()
        output_data.clear()

        slots = pmb.prompt(
            text='How many slots in recipe?',
            title='PyAutoGUI',
            default='1'
        )

        if slots is None:
            continue

        try:
            slots = int(slots)
        except ValueError:
            pmb.alert('Please enter a valid number.')
            continue

        # ---- INPUT SLOTS ----
        for i in range(slots):
            pmb.alert(
                text=f'Setting up slot {i + 1}',
                title='PyAutoGUI - INPUT',
                button='OK'
            )

            slot = {}

            slot['input'] = capture_position(
                f"[Slot {i + 1}] Where is INPUT?",
                'INPUT - Slot ' + str(i + 1)
            )

            slot['input_to'] = capture_position(
                f"[Slot {i + 1}] Where to PUT INPUT?",
                'INPUT - Slot ' + str(i + 1)
            )

            recipes.append(slot)

        # ---- SHARED OUTPUT ----
        pmb.alert(
            text='Now set OUTPUT positions (used for all slots)',
            title='PyAutoGUI - OUTPUT',
            button='OK'
        )

        output_data['output'] = capture_position(
            "Where is OUTPUT?",
            'OUTPUT'
        )

        # output_data['output_to'] = capture_position(
        #     "Where to PUT OUTPUT?"
        # )

        # ===== RUN PHASE =====
        paused = False
        listener = keyboard.Listener(on_press=on_press) # type: ignore
        listener.start()

        print('Automation started. Press ESC to pause.')

        while not paused:
            for slot in recipes:
                if paused:
                    break

                # Input → Input destination
                pag.moveTo(slot['input'])
                pag.rightClick()
                pag.moveTo(slot['input_to'])
                pag.click()

                # Shared output → output destination
                pag.moveTo(output_data['output'])
                # pag.click()
                # pag.moveTo(output_data['output_to'])
                try:
                    with pag.hold('ctrl'), pag.hold('shift'):
                        pag.press('q')

                finally:
                    pag.keyUp('shift')
                    pag.keyUp('ctrl')


                time.sleep(1)

            time.sleep(1)

        listener.join()
        print('Automation paused.')

print('Program exited.')
