import subprocess
import pty
import os


# Create a new pseudo-terminal (pty)
master, slave = pty.openpty()

# Start the shell process
shell_process = subprocess.Popen(['bash'], stdin=slave, stdout=slave, stderr=slave, start_new_session=True)

# Close the slave file descriptor in the parent process
os.close(slave)

# Main shell loop
while True:
    try:
        # Read user input
        user_input = input("$ ")

        # Send the user input to the shell process
        os.write(master, user_input.encode() + b'\n')

        # Read the shell output
        output = os.read(master, 1024).decode()

        # Print the shell output
        print(output.strip())

    except EOFError:
        # If the user presses Ctrl+D (EOF), exit the shell
        break

# Terminate the shell process
shell_process.terminate()
