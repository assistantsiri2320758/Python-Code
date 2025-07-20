# Simple CLI Calculator

def cli_calculator():
    print("Simple CLI Calculator")
    print("Enter 'quit' to exit\n")
    
    while True:
        expression = input("Enter expression (e.g., 2 + 3): ")
        
        if expression.lower() == 'quit':
            print("Goodbye!")
            break
            
        try:
            # Evaluate the expression safely
            allowed_chars = set('0123456789+-*/. ()')
            if not all(char in allowed_chars for char in expression):
                print("Error: Only numbers and + - * / operators allowed")
                continue
                
            result = eval(expression)
            print(f"Result: {result}\n")
        except ZeroDivisionError:
            print("Error: Division by zero")
        except:
            print("Error: Invalid expression")

if __name__ == "__main__":
    cli_calculator()