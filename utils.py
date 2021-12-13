import os

def generate_files(days):
    for d in days:
        day = 'day{}'.format(d)
        os.mkdir(day)
        sample_fn = 'sample{}.txt'.format(d)
        input_fn = 'input{}.txt'.format(d)
        with open(day + "/" + sample_fn, 'w') as f: pass
        with open(day + "/" + input_fn, 'w') as f: pass 
        for i in range(2):
            with open(day + "/" + 'puzzle{}.py'.format(d * 2 - i), 'w') as f:
                f.write('sample = True\n')
                f.write('file = "{}" if sample else "{}"\n'.format(sample_fn, input_fn))
                f.write('with open(file, "r") as f:\n')
                f.write('    for line in f:\n')
                f.write('        pass\n')

def main():
    generate_files([13])

if __name__ == '__main__':
    main()
