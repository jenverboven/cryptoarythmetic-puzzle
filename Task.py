# oplossing gebaseerd op tweede voorbeeld uit de cursus
import streamlit as st
import pandas as pd
import numpy as np

st.title('Cryptoarithmetic puzzle')

# import de simpleai library
from simpleai.search import CspProblem, backtrack

# vraag de user om een puzzel in te geven in het formaat "factor1 + factor2 = factor3"
expression = st.text_input('cryptoarythmetic puzzle (like "two + two = four")')

if expression:
    expression = expression.lower()
    # expression = input("Enter cryptoarythmetic puzzle (like two + two = four): ").lower()

    # maak een lijst dat alle delen van de puzzel bevat (dus de zonet gevraagde puzzel opgesplitst op de spaties)
    parts = expression.split()
    # haal uit de lijst van delen alle WOORDEN
    words = [parts[0], parts[2], parts[4]]
    # zet een lijst klaar met mogelijke operations dat de gebruiker mag invullen in de puzzel
    operators = ['+', '-', '*', '/']
    # zet een lege lijst klaar waar straks de unieke karakters uit de puzzel in terecht komen
    variables = []
    # zet een lege dictionary klaar waar straks de domains in komen, in domains komt te staan welke karakters welke numerieke waarden kunnen aannemen bij het oplossen van de puzzel
    domains = {}

    # loop door alle woorden in de puzzel
    for word in words:

        # als de eerste letter van het woord nog niet in de lijst met variabelen zit --> voeg hem toe
        if word[0] not in variables:
            variables.append(word[0])

        # als een letter voorkomt als eerste letter van een woord, ongeacht of de letter al in de lijst zit of niet, mag deze letter niet de waarde 0 aannemen
        domains[word[0]] = list(range(1, 10))

        # loop door alle letters in het woord uitgezonderd de eerste letter
        for letter in word[1:]:

            # als de letter nog niet in de variables lijst zit --> voeg hem toe aan variables en aan domains, deze letters mogen wel de waarde 0 aannemen
            if letter not in variables:
                variables.append(letter)
                domains[letter] = list(range(0, 10))


    # als er te veel verschillende karakters worden gebruikt in de puzzel krijgt de gebruiker een notificatie en wordt de puzzel niet berekend
    if len(variables) > 10:
        print("too many different characters used, use max 9 different characters")

    # als er een niet gekende operatie wordt uitgevoerd (die niet in de operations lijst staat) krijgt de gebruiker een notificatie en wordt de puzzel niet berekend
    elif parts[1] not in operators:
        print("please choose one of these operators: +, -, *, /")

    # als de vorige 2 exceptions niet voorkomen kan de puzzel berekend worden
    else:

        # een constraint om ervoor te zorgen dat alle vershillende letters maar 1 keer voorkomen in de variables lijst
        def constraint_unique(variables, values):
            return len(values) == len(set(values))  # remove repeated values and count

        # constraint om vast te leggen hoe de numerieke waarde voor elk karakter berekend moet worden op basis van de ingegeven puzzel
        def constraint_operation(variables, values):
            factors = {}

            # loop om over alle woorden in de puzzel te loopen
            for i in range(3):
                word = words[i]
                stringNumber = ""

                # loop door alle letters in het woord en maak een string waarin de letters van het woord worden vervangen door een cijfer dat mogelijks een oplossing kan zijn
                for letter in word:
                    stringNumber += str(values[variables.index(letter)])

                # zet de net geconstrueerde string om in zijn integer waarde en voeg die waarde toe aan de factors dictionary
                factors[f"factor{i + 1}"] = int(stringNumber)

            # ga na op basis van de ingegeven operatie of de puzzel overeenkomt met de geprobeerde waarden van hierboven of niet
            if parts[1] == '+':
                return (factors["factor1"] + factors["factor2"]) == factors["factor3"]
            elif parts[1] == '-':
                return (factors["factor1"] - factors["factor2"]) == factors["factor3"]
            elif parts[1] == '*':
                return (factors["factor1"] * factors["factor2"]) == factors["factor3"]
            elif parts[1] == '/':
                return (factors["factor1"] / factors["factor2"]) == factors["factor3"]

        # stel een lijst van constraints op met de verkregen karakters
        constraints = [
            (tuple(variables), constraint_unique),
            (tuple(variables), constraint_operation),
        ]

        # definieer het probleem dat we willen oplossen op basis van de door ons gedefinieerde variables, domains en constraints
        problem = CspProblem(tuple(variables), domains, constraints)

        # backtrack de tree van mogelijke oplossingen tot de uitkomst van de puzzel klopt
        output = backtrack(problem)

        longest = words[0]

        # bekijk welk woord in de puzzel het langste is om de output van het programma straks te formatteren
        for word in words:
            if len(word) > len(longest):
                longest = word

        # bepaal hoe lang de breuklijn in de output moet zijn op basis van het langste woord in de puzzel
        lineLength = len(longest) + 3

        # een functie om een woord af te printen als zijn overeenkomstig getal, gebaseerd op de oplossing van de puzzel
        def print_number(word):
            stringNumber = ""
            for letter in word:
                stringNumber += str(output[letter])
            return stringNumber

        # print de uitkomst geformatteerd af
        lines = [
            " " * (lineLength - len(words[0])) + words[0].upper() + " " * (8 + (lineLength - len(words[0]))) + print_number(words[0]),
            parts[1] + " " * (lineLength - (len(words[1]) + 1)) + words[1].upper() + " " * 8 + parts[1] + " " * (lineLength - len(words[1]) - 1) + print_number(words[1]),
            "-" * lineLength + "  --->  " + "-" * lineLength,
            " " * (lineLength - len(words[2])) + words[2].upper() + " " * (8 + lineLength - len(words[2])) + print_number(words[2])
        ]

        for line in lines:
            st.text('                   ' + line)

        # leading_spaces = f"""           My name is and I am years old."""
        # st.write(leading_spaces, unsafe_allow_html=True)

        print(" " * (lineLength - len(words[0])) + words[0].upper() + " " * (8 + (lineLength - len(words[0]))) + print_number(words[0]))
        print(parts[1] + " " * (lineLength - (len(words[1]) + 1)) + words[1].upper() + " " * 8 + parts[1] + " " * (lineLength - len(words[1]) - 1) + print_number(words[1]))
        print("-" * lineLength + "  --->  " + "-" * lineLength)
        print(" " * (lineLength - len(words[2])) + words[2].upper() + " " * (8 + lineLength - len(words[2])) + print_number(words[2]))