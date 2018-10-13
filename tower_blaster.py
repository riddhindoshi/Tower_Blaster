import random
# used for clearing the screen when required to give real game feel
import os
# import time


def shuffle(bricks):
    """This function is used to shuffle the input bricks given. Return: None"""
    random.shuffle(bricks)


def check_bricks(main_pile, discard):
    """This function checks if there are any cards left in the main pile. If there are no cards left,
    it will shuffle the discard pile and place it in the main pile. Return: None"""
    if not main_pile:
        shuffle(discard)
        main_pile = discard.copy()
        # unsure about this
        discard[0] = main_pile[0]


def check_tower_blaster(pile):
    """This function checks if stability of a tower(tower in ascending order) is achieved.
    Return: True if achieved, False if not"""
    # the sort function will lay out bricks in ascending order
    if sorted(pile) == pile:
        return True
    return False


def get_top_brick(brick_pile):
    """This function removes the top brick from any pile given as an input. Return: The value at the top brick"""
    top_brick = brick_pile[0]
    # removes the top brick from the pile to be added somewhere else
    del brick_pile[0]
    # returns the top brick
    return top_brick


def deal_initial_bricks(main_pile):
    """This function starts the game by dealing two sets of 10 bricks each. Return: 2 lists, one representing the user’s
    hand and the other representing the computer’s hand"""
    user_pile = []
    computer_pile = []
    shuffle(main_pile)
    # Deal the 20 bricks from main pile
    for i in range(0, 20):
        # ensures alternate bricks dealt to computer and user, computer first
        if i % 2 == 0:
            computer_pile.insert(0, main_pile[i])
        else:
            user_pile.insert(0, main_pile[i])
    del main_pile[0:20]

    return user_pile, computer_pile


def add_brick_to_discard(brick, discard):
    """This function adds the brick to the top of discard pile. Return: None"""
    discard.insert(0, brick)


def find_and_replace(new_brick, brick_to_be_replaced, pile, discard):
    """This function finds the brick to be replaced in the tower and replaces it with new_brick.
    Return: True if brick is replaced, False if not"""
    for i, brick in enumerate(pile):
        # find where the brick is to be replaced
        if brick == brick_to_be_replaced:
            pile[i] = new_brick
            # insert the old brick to the discard file
            discard.insert(0, brick_to_be_replaced)
            return True
    return False


def computer_play(computer_pile, main_pile, discard):
    """This function is where the computer(programmer) makes its move"""
    # The strategy here is:
    # The computer will always take from discard pile and play safe, main_pile is unused
    # It would only place bricks 1-10 on the top 0,1 levels
    # It would only place bricks 10-30 on the top 2,3,4 levels
    # It would only place bricks 30-40 on the top 5,6 levels
    # It would only place bricks 40-60 on the top 7,8,9 levels
    # The placement would depend on the present tower the computer has
    # It focuses on first maintaining all the levels as described and discarding the unrequired blocks
    # Then it would focus on building a tower by replacing the splits in levels
    # described and sorting the individual levels in ascending order
    # Once all the bricks are sorted in ascending order, the computer will win

    # FEW REQUIRED ASSUMPTIONS:
    # The user does not reject the same pile twice!! (May be a huge one, but was required for this strategy to work)

    new_brick = discard[0]

    # split the computer pile into 4 sections and work on getting each section sorted individually
    list1, list2, list3, list4 = computer_pile[0:2], computer_pile[2:5], computer_pile[5:7], computer_pile[7:10]
    lowest_brick_list4 = min(list4)
    lowest_brick_list3 = min(list3)
    lowest_brick_list2 = min(list2)
    lowest_brick_list1 = min(list1)

    highest_brick_list3 = max(list3)
    highest_brick_list2 = max(list2)
    highest_brick_list1 = max(list1)

    # Always let 1 be the topmost brick
    if new_brick == 1:
        find_and_replace(new_brick, computer_pile[0], list1, discard)

    # Always let 60 be the bottommost brick
    elif new_brick == 60:
        find_and_replace(new_brick, computer_pile[9], list2, discard)

    # This range of bricks would work on list4
    elif 40 <= new_brick <= 59:
        if lowest_brick_list4 < new_brick or 40 <= lowest_brick_list4 <= 59:
            print(lowest_brick_list4)
            if list4 != sorted(list4) or lowest_brick_list4 >= 40:
                find_and_replace(new_brick, lowest_brick_list4, list4, discard)

    # This range of bricks would work on list3
    elif 30 <= new_brick < 40:
        if lowest_brick_list3 < new_brick or 30 <= lowest_brick_list3 < 40 or highest_brick_list3 > 40:
            if highest_brick_list3 > 40:
                find_and_replace(new_brick, highest_brick_list3, list3, discard)
            elif list3 != sorted(list3) or lowest_brick_list3 >= 30:
                find_and_replace(new_brick, lowest_brick_list3, list3, discard)

    # This range of bricks would work on list2
    elif 10 <= new_brick < 30:
        if lowest_brick_list2 < new_brick or 10 <= lowest_brick_list2 < 30 or highest_brick_list2 > 30:
            if highest_brick_list2 > 30:
                find_and_replace(new_brick, highest_brick_list2, list2, discard)
            elif list2 != sorted(list2) or lowest_brick_list2 >= 10:
                find_and_replace(new_brick, lowest_brick_list2, list2, discard)

    # This range of bricks would work on list1
    elif 2 <= new_brick < 10:
        if lowest_brick_list1 < new_brick or 2 <= lowest_brick_list1 < 10 or highest_brick_list1 > 10:
            if highest_brick_list1 > 10:
                find_and_replace(new_brick, highest_brick_list1, list1, discard)
            elif list1 != sorted(list1) or lowest_brick_list1 >= 2:
                find_and_replace(new_brick, lowest_brick_list1, list1, discard)

    computer_pile = list1 + list2 + list3 + list4
    return computer_pile


def print_vertical(my_list):
    """This helper function prints the towers vertically for better visualization. Return: None"""
    for i in my_list:
        print(i)


def clear():
    """This function is used to clear the screen of terminal. Return: None"""
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def view_user_pile(name, user_pile):
    """This function is used to view the user pile on the screen of terminal. Return: None"""
    print(name, "'s Pile:")
    print_vertical(user_pile)


def move_main_to_discard(main_pile, discard):
    """This function moves the brick from the top of the main pile to the top of the discard pile. Return: None"""
    add_brick_to_discard(main_pile[0], discard)
    del main_pile[0]


def view_discard_pile_top(discard):
    """This function is used to view the top brick of discard pile on the screen of terminal. Return: None"""
    print("Discard pile top is: ", discard[0])


def update_tower_from_discard_pile(discard, user_pile):
    new_brick = discard[0]
    brick_to_be_replaced = int(input("Enter the brick you want to replace"))
    while not find_and_replace(new_brick, brick_to_be_replaced, user_pile, discard):
        print("The brick you entered is not present in your tower."
              "Please enter a valid brick to be replaced")
        brick_to_be_replaced = int(input("Enter the brick you want to replace "))
    print("Success!! Your brick was replaced.. Please wait for your turn")


def update_tower_from_main_pile(new_brick, discard, user_pile):
    brick_to_be_replaced = int(input("Enter the brick you want to replace"))
    while not find_and_replace(new_brick, brick_to_be_replaced, user_pile, discard):
        print("The brick you entered is not present in your tower."
              "Please enter a valid brick to be replaced")
        brick_to_be_replaced = int(input("Enter the brick you want to replace "))
    print("Success!! Your brick was replaced.. Please wait for your turn")


def main():
    # pre-initialize game text
    print("Let's begin Tower Blaster!!!")
    print("Your Mission: You have to help the Greeks to build a tower before the Vikings,"
          "because they have started a tower building contest.")
    input("Should you choose to accept? Press Enter to BEGIN!!...")
    name = input("\nNickname: ")

    # initialize game parameters
    # initialize main pile from 1-60
    main_pile = list(range(1, 61))
    # populate user_pile and computer_pile
    user_pile, computer_pile = deal_initial_bricks(main_pile)
    # initialize empty discard pile
    discard = []

    # Show initial piles to the user
    view_user_pile(name, user_pile)
    print("Viking's Pile: ")
    print_vertical(computer_pile)
    print("The Tower Numbers go from 1 to 60\n")
    input("Press Enter to continue...")
    clear()
    move_main_to_discard(main_pile, discard)

    # Begin game here
    while not check_tower_blaster(user_pile) or check_tower_blaster(computer_pile):
        view_user_pile(name, user_pile)
        view_discard_pile_top(discard)
        decision = input("Do you want to choose this to use this Brick? Say Y or N: ")

        if decision == 'Y':
            update_tower_from_discard_pile(discard, user_pile)

        if decision == 'N':
            clear()
            # check if main pile is empty
            check_bricks(main_pile, discard)
            print("Main pile top is:", main_pile[0])
            decision = input("Do you want to choose this to use this Brick? Say Y or N: ")
            if decision == 'Y':
                update_tower_from_main_pile(main_pile[0], discard, user_pile)
                print("Your updated tower is:")
            if decision == 'N':
                print("Okay! No change was made to your tower. Please wait for your next turn")

        # computer's turn!!
        computer_pile = computer_play(computer_pile, main_pile, discard)


if __name__ == "__main__":
    main()





