def print_christmas_tree(height):
    """
    Function to print a simple Christmas tree with "*" characters
    and one "#" character at the bottom as the trunk.
    
    Parameters:
    height (int): The height of the Christmas tree (number of levels).
    """
    
    # Loop through each level of the tree
    for i in range(height):
        # Print spaces to center the tree
        # The number of spaces is (height - i - 1)
        print(' ' * (height - i - 1), end='')
        
        # Print the "*" characters for the current level
        # The number of "*" characters is (2 * i + 1)
        print('*' * (2 * i + 1))
    
    # Print the trunk of the tree
    # The trunk is centered, so print (height - 1) spaces and then "#"
    print(' ' * (height - 1) + '#')

# Example usage:
print_christmas_tree(5)

print("test" * 5)