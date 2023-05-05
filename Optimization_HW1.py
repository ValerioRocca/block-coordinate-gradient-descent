from xml.dom import pulldom
import numpy as np
import matplotlib.pyplot as plt

# Part 1: point generation (10000 points (5000 per class), 5% labeled)
# Set up parameters for the L shape
mu1 = np.array([-2, 0])
mu2 = np.array([2, 4])
mu3 = np.array([2, 11])
mu4 = np.array([-2, 7])
sigma1 = np.array([[7, 0], [0, 0.5]])
sigma2 = np.array([[0.5, 0], [0, 4]])  # Modified standard deviation for sample 2
sigma3 = np.array([[7, 0], [0, 0.5]])
sigma4 = np.array([[0.5, 0], [0, 4]])  # Modified standard deviation for sample 4
weights = [0.25, 0.25, 0.25, 0.25]

# Generate random points in the L shape using the Bivariate Gaussian Mixture Distribution
n_points = 1000 #change to 10000
samples1 = np.random.multivariate_normal(mu1, sigma1, int(n_points*weights[0]))
samples2 = np.random.multivariate_normal(mu2, sigma2, int(n_points*weights[1]))
samples3 = np.random.multivariate_normal(mu3, sigma3, int(n_points*weights[2]))
samples4 = np.random.multivariate_normal(mu4, sigma4, int(n_points*weights[3]))

# Assign class labels to the samples
# class1 = np.concatenate((samples2, samples1))
class1 = np.concatenate((samples2, samples1))
class1 = np.c_[class1, np.zeros(len(class1))]
count = 0
for i in class1:
  if count == 19:
    count = 0
    i[2] = 1
  count += 1
class2 = np.concatenate((samples3, samples4))
class2 = np.c_[class2, np.zeros(len(class2))]
count = 0
for i in class2:
  if count == 19:
    count = 0
    i[2] = -1
  count += 1

# Combine the samples of all three classes
all_samples = np.concatenate((class1, class2))

# Split the samples based on their class label
unlabeled_samples = all_samples[all_samples[:,2] == 0]
class1_samples = all_samples[all_samples[:,2] == 1]
class2_samples = all_samples[all_samples[:,2] == -1]

# Labeled matrix
labeled_samples = np.concatenate((class1_samples, class2_samples))

# Assign random label to unlabeled units
random_unlabeled = unlabeled_samples
random_unlabeled[:,2] = np.random.choice([-1, 1], size=(len(unlabeled_samples),)) 

# Plot the samples of each class with a different color and marker
plt.scatter(unlabeled_samples[:,0], unlabeled_samples[:,1], color='grey', label='Unlabeled', alpha=0.5)
plt.scatter(class1_samples[:,0], class1_samples[:,1], color='red', label='Label 1', alpha=0.5)
plt.scatter(class2_samples[:,0], class2_samples[:,1], color='blue', label='Label -1', alpha=0.5)

# Add legend and axis labels
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')

# Show the plot
#plt.show()

# ---------------------------------------------------------------

# Part 2: similarity function distance = numpy.linalg.norm(a-b)
#a = np.array([1, 2, 3])
#b = np.array([4, 5, 6])
#distance = np.linalg.norm(a-b)
#print(distance)

w = np.zeros((np.shape(unlabeled_samples)[0], np.shape(labeled_samples)[0]))
w_bar = np.zeros((np.shape(unlabeled_samples)[0], np.shape(unlabeled_samples)[0]))

# similarity matrix unlabeled-labeled
for row in range(np.shape(w)[0]):
  for col in range(np.shape(w)[1]):
    w[row,col] = np.linalg.norm(unlabeled_samples[row,0:1] - labeled_samples[col,0:1])

# similarity matrix unlabeled-unlabeled
for row in range(np.shape(w_bar)[0]):
  for col in range(np.shape(w_bar)[1]):
    w_bar[row,col] = np.linalg.norm(unlabeled_samples[row,0:1] - unlabeled_samples[col,0:1])

#-----------------------------------------------------------------------
# Part 3: 

# w.shape = (948,52)
# w_bar.shape = (948,948)
# labeled_samples.shape = (52,3)
# unlabeled_samples.shape = (948,3)

def gradient_iterative(lab_samples, unlab_samples, w=w, w_bar=w_bar):
  grads = []
  for j in range(np.shape(unlab_samples)[0]): # Da 0 a 947
      grad = 0
      for i in range(np.shape(lab_samples)[0]):
          grad += w[j][i] * (unlab_samples[j][2] - lab_samples[i][2])
      for i in range(np.shape(unlab_samples)[0]):
          grad += w_bar[j][i] * (unlab_samples[j][2] - unlab_samples[i][2])
      grads.append(2 * grad)
  return np.array(grads)

print(gradient_iterative(labeled_samples, unlabeled_samples))

print(gradient_iterative(labeled_samples, unlabeled_samples).shape)