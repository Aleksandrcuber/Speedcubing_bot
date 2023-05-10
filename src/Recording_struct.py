class Record:
    def __init__(self, string):
        string = string.strip()

        if string[0] in ['.', ':']:
            string = '0' + string

        result = str()
        self.comment = str()
        i = 0
        while i < len(string) and string[i] not in [' ', ';', ',']:
            result += string[i]
            i += 1
        i += 1
        self.comment = string[i:]
        self.comment = self.comment.strip()

        arr_of_strs = []
        curr = ''
        for elem in result:
            if elem not in [".", ":"]:
                curr += elem
            else:
                arr_of_strs.append(curr)
                if not curr.isdigit():
                    raise ValueError
                curr = ''
        arr_of_strs.append(curr)
        if len(arr_of_strs) > 3 or len(arr_of_strs) < 2:
            raise ValueError

        for i in range(1, len(arr_of_strs)):
            if len(arr_of_strs[i]) != 2:
                raise ValueError
        self.mils = int(arr_of_strs[-1])
        self.seconds = int(arr_of_strs[-2])
        if self.seconds > 59:
            raise ValueError
        if len(arr_of_strs) == 3:
            self.minutes = int(arr_of_strs[0])
        else:
            self.minutes = 0

    def __str__(self):
        if self == Record("100000:00:00"):
            return ''
        if self.mils < 10:
            answer = f".0{str(self.mils)}"
        else:
            answer = f".{str(self.mils)}"
        if self.minutes > 0:
            if self.seconds < 10:
                seconds = '0' + str(self.seconds)
            else:
                seconds = str(self.seconds)
            answer = f"{str(self.minutes)}:{seconds}" + answer
            return answer + (' - ' + self.comment) * (self.comment != '')
        return str(self.seconds) + answer + (' - ' + self.comment) * (self.comment != '')

    def __int__(self):
        return self.minutes * 6000 + self.seconds * 100 + self.mils

    def __eq__(self, other):
        return int(self) == int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return other > self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not self > other

    def __add__(self, other):
        return from_number(int(self) + int(other))

    def __sub__(self, other):
        return from_number(int(self) - int(other))

    def __truediv__(self, other):
        return from_number(int(self) / other)


def from_number(num):
    num = int(num)
    result = Record("0:00:00")
    result.mils = num % 100
    num //= 100
    result.seconds = num % 60
    result.minutes = num // 60
    return result


def count_avg(lst, n):
    if len(lst) < n:
        return Record("100000:00:00")
    arr = lst[-n:]
    summ = Record("0:00:00")
    for elem in arr:
        summ += elem
    return (summ - min(arr) - max(arr)) / (n - 2)
