class UtilityBot:

    @staticmethod
    def chunk_arr(arr, fill_value, chunk_length=None):
        """
        Transforms an array into a 2-dimensional array
        :param arr: Array to transform
        :param fill_value: Value to fill gaps in child array
        :param chunk_length: Length of child array
        :return: Array
        """
        new_arr = []
        i = 0
        while i <= len(arr) - 1:
            child_arr = []
            for j in range(chunk_length):
                if i <= len(arr) - 1:
                    child_arr.append(arr[i])
                elif chunk_length is not None:
                    child_arr.append(fill_value)
                i += 1
            new_arr.append(child_arr)
        return new_arr
