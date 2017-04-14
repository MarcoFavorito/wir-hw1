import matplotlib.pyplot as plt
import numpy as np
import file_parser
import sys

def print_usage():
	print("Usage: \n")
	print("make_plot.py out_filename plot_title <label1> <scores_filename1> <label2> <scores_filename2>")

def main():
	"""
	Takes in input a file with the format:
	[label\tscore]
	:return:
	"""

	if len(sys.argv) < 5 and len(sys.argv)%2!=1:
		print_usage()
		return -1


	out_filename = sys.argv[1]
	plot_title = sys.argv[2]
	labels = sys.argv[3::2]
	scores_filename_list = sys.argv[4::2]


	scores_lists = []
	lines = []

	for file in scores_filename_list:
		with open(file) as f:
			scores_list = file_parser.file2list(f, [int, float])
			scores_lists.append(scores_list)

	for i, scores_list in enumerate(scores_lists):
		x, y = zip(*scores_list)
		xlabels = list(map(str, x))
		ind = np.arange(len(y))

		cur_line, = plt.plot(ind, y, label=labels[i])
		lines.append(cur_line)
		plt.xticks(ind, xlabels)

	plt.legend(lines, labels)
	plt.title(plot_title)
	plt.grid()
	plt.savefig(out_filename+".svg")




if __name__ == "__main__":
	main()


