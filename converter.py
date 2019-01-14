if __name__ == '__main__':
    with open('5syllables.txt') as f:
        lines = f.readlines()

    j = 0
    offset = 20
    while j < len(lines):
        index = int(lines[j+3][12])
        mp3 = (j / 10 + 1 + offset)
        options = [line.strip() for line in lines[j+5:j+8+1]]
        answer = lines[j+8+1].strip().split()[1]
        options.append(answer)
        all_options = ["'" + option + "'" for option in options]
        print("q%d = {\n\t'i' : %d,\n\t'mp3_url' : '%d.mp3',\n\t'options' : [%s],\n\t'answer' : '%s'\n};" % (mp3, index, mp3, ', '.join(all_options), answer))
        j += 10
