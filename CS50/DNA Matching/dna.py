import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage : dna.py database sequence")
        return 1
    # Read database file into a variable
    database_ptr = sys.argv[1]
    with open(database_ptr) as database:
        reader = csv.reader(database)
        header = []
        header = next(reader)
        rows = []
        for row in reader:
            rows.append(row)

    # Read DNA sequence file into a variable
    dna_ptr = open(sys.argv[2], "r")
    sequence = dna_ptr.read()

    # Find longest match of each STR in DNA sequence
    strs = []
    for i in range(1, len(header), 1):
        str_name = header[i]
        longest_run = longest_match(sequence, str_name)
        pair = (str_name, longest_run)
        strs.append(pair)

    # Check database for matching profiles

    isbreak = False
    match = False
    for row in rows:
        row_index = 1
        str_index = 0
        if isbreak == False:
            while(int(row[row_index]) == int(strs[str_index][1])):
                checkrowindex = row_index
                if row_index == len(row) - 1:
                    match = True
                    match_name = row[0]
                    isbreak = True
                    break
                row_index += 1
                str_index += 1
    if match == True:
        print(match_name)
    else:
        print("No Match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
