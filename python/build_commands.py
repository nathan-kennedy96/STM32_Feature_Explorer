from pathlib import Path


def update_python_commands() -> None:
    """
    Update the command.py python file from the contents of command.h
    """

    this_dir = Path(__file__).parent
    top_level_dir = this_dir.parent
    command_header_path = top_level_dir / "stm32" / "Core" / "Inc" / "command.h"

    text_data = command_header_path.read_text()
    # get text between {}
    target_text = text_data.split("{")[-1].split("}")[0]
    # no commas in the python implementation
    fixed_text = target_text.replace(",", "")

    # Write the text
    target_file = this_dir / "command.py"
    target_file_contents = f"""from enum import Enum

class Command(Enum):
    {fixed_text}
    """
    target_file.write_text(target_file_contents)


if __name__ == "__main__":
    update_python_commands()
