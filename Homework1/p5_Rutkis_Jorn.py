
def ceaser_cypher(text, shift):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            if char.isupper():
                base = ord("A") 
            else:
                base = ord("a")
            char = chr((ord(char) - base + shift) % 26 + base)
        result += char
    return result

def ceaser_decipher(cyphertext, shift):
    result = ""

    for i in range(len(cyphertext)):
        char = cyphertext[i]
        if char.isalpha():
            if char.isupper():
                base = ord("A") 
            else:
                base = ord("a")
            char = chr((ord(char) - base - shift) % 26 + base)

        result += char
    return result 

def main():

    input_str = input("Please enter ur string: ")
    shift_str = input("Please enter the shift value:")
    shift = int(shift_str)

    output = ceaser_cypher(input_str, shift)
    print("Your encrypted string: ", output)

    decyp_str = input("Please enter the string you want to decrypt: ")
    unshift_str = input("Please enter the shift value:")
    unshift = int(unshift_str)

    output_dec = ceaser_decipher(decyp_str, unshift)
    print("Your decrypted string: ", output_dec)

main()