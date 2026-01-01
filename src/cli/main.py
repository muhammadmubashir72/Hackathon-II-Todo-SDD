"""
CLI module for Todo Console Application
Handles user interaction, menu display, and command processing
"""

from src.services.task_service import TaskService
from src.skills.input_parsing import parse_menu_selection, parse_task_id, parse_text_input
from src.skills.task_formatting import format_main_menu


def display_main_menu() -> None:
    """Display main menu options"""
    menu = format_main_menu()
    print(menu)


def get_user_choice() -> str:
    """Get and normalize user menu selection"""
    choice_input = input("Your choice: ")
    return choice_input.strip()


def handle_choice(choice: str, task_service: TaskService) -> None:
    """
    Handle user menu choice and execute appropriate action

    Args:
        choice: User's menu selection
        task_service: TaskService instance
    """
    # Handle numeric input for menu options
    try:
        choice_num = int(choice)
    except ValueError:
        # Non-numeric input - show menu again
        print(f"\nInvalid selection: '{choice}'. Please choose between 1 and 7.")
        return

    if choice_num == 1:
        # Add task
        print(f"\n{'─' * 60}")
        print("ADD TASK")
        print(f"{'─' * 60}")
        title_input = input("Enter task title: ")
        description_input = input("Enter description (optional, press Enter to skip): ")
        print(task_service.create_task(title_input, description_input))

    elif choice_num == 2:
        # View tasks
        print(task_service.view_tasks())

    elif choice_num == 3:
        # Update task
        print(f"\n{'─' * 60}")
        print("UPDATE TASK")
        print(f"{'─' * 60}")
        task_id_input = input("Enter task ID: ")
        new_title_input = input("Enter new title (optional, press Enter to skip): ")
        new_desc_input = input("Enter new description (optional, press Enter to skip): ")

        # Determine what to update
        title = new_title_input if new_title_input.strip() else None
        description = new_desc_input if new_desc_input.strip() else None

        print(task_service.update_task(int(task_id_input.strip()), title, description))

    elif choice_num == 4:
        # Delete task
        print(f"\n{'─' * 60}")
        print("DELETE TASK")
        print(f"{'─' * 60}")
        task_id_input = input("Enter task ID: ")
        confirm_input = input("Confirm deletion (y/N): ").strip().lower()

        confirmed = confirm_input in ['y', 'yes']
        print(task_service.delete_task(int(task_id_input.strip()), confirmed))

    elif choice_num == 5:
        # Mark complete
        print(f"\n{'─' * 60}")
        print("MARK TASK COMPLETE")
        print(f"{'─' * 60}")
        task_id_input = input("Enter task ID: ")
        print(task_service.mark_complete(int(task_id_input.strip())))

    elif choice_num == 6:
        # Mark incomplete
        print(f"\n{'─' * 60}")
        print("MARK TASK INCOMPLETE")
        print(f"{'─' * 60}")
        task_id_input = input("Enter task ID: ")
        print(task_service.mark_incomplete(int(task_id_input.strip())))

    elif choice_num == 7:
        # Exit application
        print(f"\n{'=' * 60}")
        print("Thank you for using Todo CLI!")
        print(f"{'=' * 60}")
        print("Goodbye!")
        exit(0)

    else:
        # Invalid selection
        print(f"\nInvalid selection: {choice_num}. Please choose between 1 and 7.")


def main() -> None:
    """
    Main CLI entry point
    Runs main menu loop until user exits
    """
    task_service = TaskService()

    while True:
        # Display main menu
        display_main_menu()

        # Get user choice
        choice = get_user_choice()

        # Handle choice
        handle_choice(choice, task_service)

        print("\n")  # Blank line for readability


if __name__ == "__main__":
    main()
