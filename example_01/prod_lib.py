# prod_lib.py - module with better_name function

def better_name(first_name, second_name):
    full_name = first_name + " " + second_name
    print(full_name.title())

# New function that returns the formatted name instead of printing it
# Returned string should not contain more than 15 characters
def better_name_return(first_name, second_name):
    # Build the full name and normalize whitespace
    full_name = (str(first_name).strip() + " " + str(second_name).strip()).strip()
    formatted = full_name.title()
    # Ensure the returned string is at most 15 characters
    if len(formatted) > 15:
        return formatted[:15]
    return formatted