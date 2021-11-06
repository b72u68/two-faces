from subprocess import run


class GenFiles:

    def __init__(self, filename: str, tag: str = "A", num_tags: int = 200):
        '''
        Initialize the inputs.

        filename: str
        tag: str
        num_tags: int
        '''

        assert len(tag) == 1, "Tag length has to be 1."
        assert int(num_tags) >= 100, "Number of tags in an array has to be at least 100."

        self.BYTE_STREAM = []
        self.FILENAME = filename
        self.TAG = hex(ord(tag))
        self.NUM_TAGS = num_tags
        self.RESULT_DIR = ".two_faces_result"

    def read_byte_stream(self):
        '''
        Get byte stream from the input file.
        '''
        try:
            with open(self.FILENAME, "rb") as f:
                self.BYTE_STREAM = f.read()
            f.close()
        except Exception as e:
            print(e)

    def get_tag_arrays_location(self):
        '''
        Get locations of two tag arrays in the byte stream.
        '''
        start_end = []
        for i in range(len(self.BYTE_STREAM)):
            if hex(self.BYTE_STREAM[i]) == self.TAG:
                start = end = i
                while end < len(self.BYTE_STREAM) and hex(self.BYTE_STREAM[end]) == self.TAG:
                    end += 1
                end -= 1
                if end - start + 1 == self.NUM_TAGS:
                    start_end.append((start, end))
        return start_end

    def get_array_offset(self, start: int) -> int:
        '''
        Calculate the offset from the start of the first array for the size
        of the prefix to be a multiple of 64.
        '''
        return 64 - start % 64

    def get_prefix_size(self, start: int, offset: int) -> int:
        '''
        Return the size of the prefix.
        '''
        return start + offset

    def get_suffix_size(self, byte_stream_size: int, prefix_size: int) -> int:
        '''
        Return the size of the suffix.
        '''
        return byte_stream_size - prefix_size - 128

    def clean(self):
        '''
        Clean directory.
        '''
        run(f'rm -rf {self.RESULT_DIR}', shell=True)

    def gen(self):
        '''
        Generate two files with the same MD5 hash from the given benign file
        that contains malicious code but one can execute malicious code.
        '''

        try:
            run(f'[ ! -d {self.RESULT_DIR} ] && mkdir {self.RESULT_DIR}', shell=True)

            self.read_byte_stream()

            start_end = self.get_tag_arrays_location()

            assert len(start_end) == 2, "Program has to have two tag arrays."

            s1, e1 = start_end[0]
            s2, e2 = start_end[1]

            offset = self.get_array_offset(s1)
            prefix_size = self.get_prefix_size(s1, offset)
            suffix_size = self.get_suffix_size(len(self.BYTE_STREAM), prefix_size)

            # get the prefix and the suffix of the executable file
            run(f'head -c {prefix_size} {self.FILENAME} > {self.RESULT_DIR}/prefix', shell=True)
            run(f'tail -c {suffix_size} {self.FILENAME} > {self.RESULT_DIR}/suffix', shell=True)

            # generate two files with the same md5 using prefix as prefixfile
            run(f'md5collgen -p {self.RESULT_DIR}/prefix -o {self.RESULT_DIR}/prefix_P {self.RESULT_DIR}/prefix_Q', shell=True)

            # get P and Q (the 128 bytes generate by md5collgen) from prefix_P and prefix_Q
            run(f'tail -c 128 {self.RESULT_DIR}/prefix_P > {self.RESULT_DIR}/P', shell=True)
            run(f'tail -c 128 {self.RESULT_DIR}/prefix_Q > {self.RESULT_DIR}/Q', shell=True)

            # get the starting position of Y with offset relative to starting position
            # of suffix
            # get the end position of 128 bytes from the starting position of Y with
            # offset
            s2_P = s2 - 128 - prefix_size + offset
            e2_P = s2_P + 128

            # insert P in the middle of array Y in the suffix
            run(f'head -c {s2_P} {self.RESULT_DIR}/suffix > {self.RESULT_DIR}/suffix_pre', shell=True)
            run(f'tail -c +{e2_P} {self.RESULT_DIR}/suffix > {self.RESULT_DIR}/suffix_post', shell=True)
            run(f'cat {self.RESULT_DIR}/suffix_pre {self.RESULT_DIR}/P {self.RESULT_DIR}/suffix_post > {self.RESULT_DIR}/suffix_P', shell=True)

            # concat prefix_p and prefix_Q with suffix_P to create two new executable
            # files a1.out and a2.out with the same md5 hash
            run(f'cat {self.RESULT_DIR}/prefix_P {self.RESULT_DIR}/suffix_P > a1.out', shell=True)
            run(f'cat {self.RESULT_DIR}/prefix_Q {self.RESULT_DIR}/suffix_P > a2.out', shell=True)

        except Exception as e:
            print(e)
