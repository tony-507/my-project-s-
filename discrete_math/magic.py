# Check if a given array of size n*n can form a magic square or not.
# If yes, print out the square, otherwise print a statement saying that it is impossible.
# A magic square is an n times n matrix whose row sums, column sums and diagonal sums are equal.
# It is known that for n>=3, the list [1,...,n*n] can form a magic square.

#This code asks the user to input the dimension n and the list u, then
# call check_magic to do a quick check on impossibility
# call gen_perm to compute a solution by backtracking using DFS

def check_sum(perm, n, s):
	"""This is the major function on determining magic squares."""
	# perm is a guess, n is the dimension, s is the desired sum.
	max_row = (len(perm)-1)//n
	max_col = (len(perm)-1)%n

	#print('row: ', max_row, 'col: ', max_col)

	if max_row == 0:
		# Nothing to calculate
		return True
		exit()

	# Check row sum
	for i in range(max_row):
		# The last row may not be filled
		if sum(perm[i*n:(i+1)*n]) != s:
			#print(i, ' -th row fails')
			return False

	#print("row sum ok")

	# Cases available only when all rows are filled
	if max_row == n-1:
		# Check col sum
		for j in range(max_col+1):
			if sum(perm[j::n]) != s:
				#print(j,' -th column fails')
				return False

		#print("column sum ok")

		# Check anti-diagonal
		if sum(perm[n-1:(n-1)*n+1:n-1]) != s:
			#print('anti-diagonal fails')
			return False

		#print("anti-diagonal ok")

	# Check diagonal sum and last row sum
	if len(perm) == n*n:
		#Available only when perm is filled up
		if sum(perm[0::n+1]) != s:
			#print('Diagonal fails')
			return False

		#print("diagonal ok")

		if sum(perm[(n-1)*n:n*n]) != s:
			#print('Last row fails')
			return False

	return True

def gen_perm(perm, vec, n):
	s = sum(vec)/n
	if len(perm) == n*n:
		if check_sum(perm, n, s) == True:
			display_sol(perm, n)
		else:
			perm.pop()
		exit()

	for i in range(n*n):
		if vec[i] not in perm:
			perm.append(vec[i])

			if check_sum(perm, n, s):
				gen_perm(perm, vec, n)

			perm.pop()

	if len(perm)==0:
		#All popped out, i.e. no solution
		print("This vector cannot form a magic square")

def display_sol (perm, n):
	for i in range(n):
		print(perm[i*n:(i+1)*n])

def check_magic(vec, n):
	if sum(vec)%n != 0:
		print("This vector cannot form a magic square")
	else:
		gen_perm([], vec, n)

if __name__ == "__main__":
	n = int(input('Enter the dimension: '))
	u = []
	for i in range(n*n):
		print('Enter the ', i, '-th number:')
		num = int(input())
		u.append(num)
	check_magic(u,n)