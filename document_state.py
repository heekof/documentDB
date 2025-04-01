from enum import Enum, auto

class DocumentStatus(Enum):
    ACTIVE = auto()
    HOT = auto()
    COLD = auto()
    ARCHIVE = auto()
    SOFT_DELETE = auto()


class Status(Enum):
    PENDING = auto()      # 1
    RUNNING = auto()      # 2
    COMPLETED = auto()    # 3




# Example usage

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Access by name
print(Color.RED)           # Color.RED
print(Color.RED.name)      # 'RED'
print(Color.RED.value)     # 1

# Iteration
for color in Color:
    print(color)           # prints all members

# Membership
print(Color.RED in Color)  # True