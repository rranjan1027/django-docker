class Solution:
    @staticmethod
    def letter_combinations(digits: str):
        res = []
        letter_map = {
            "2": 'abc',
            "3": 'def',
            "4": 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz'
        }

        def backtrack(i, cur_str):
            if len(cur_str) == len(digits):
                print("Same", cur_str)
                res.append(cur_str)
                return
            for c in letter_map[digits[i]]:
                print('2222', i, cur_str, c)
                backtrack(i + 1, cur_str + c)

        if digits:
            print('1111')
            backtrack(0, "")

        return res


obj = Solution()
print(obj.letter_combinations("23"))


def combination_sum(candidates, target):
    def backtrack(start, target, path):
        if target == 0:
            result.append(path)
            return
        if target < 0:
            return
        for i in range(start, len(candidates)):
            backtrack(i, target - candidates[i], path + [candidates[i]])

    result = []
    backtrack(0, target, [])
    print(result)
    return result


target = 8
candidates = [2, 3, 5]
#combination_sum(candidates, target)


#location /app
  # app

#nginx -s reload


# sudo apt insatll nginx -y

# delete the default from /etc/ngnx/site-enabled
# then create a nginx file with any name and paste the content
# sudo ln -s /etc/nginx/site-availabel/<file name> /etc/nginx/site-enabled/

# sudo gpasswd -a www-data ubuntu
# sudo systemctl restart nginx
# sudo service nginx restart



# /etc/nginx/ (for systems like Ubuntu, Debian)
# /usr/local/nginx/conf/ or /usr/local/etc/nginx/ (for systems where Nginx was installed from source or with custom configurations)