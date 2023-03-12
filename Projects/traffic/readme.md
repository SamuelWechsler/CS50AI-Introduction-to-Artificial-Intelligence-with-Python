# Video
Here's the link to the screencast that demonstartes the project's functionality: https://youtu.be/LYUI6lxsNiw.

# Increasing repetitions of convolution and pooling
Repeating 2D-convolution and max-pooling at least twice lead to a substantial increase in accuarcy estimated on the test set (≈95%) whereas performing convolution and pooling once was associated with a poor accuarcy (≈5%).

# Pooling size, size of convolutional filter
The number of convolutional filters and the size of the pooling matrix seems to optimal at 32 filters and 2x2. Increasing the number of convolutional filters didn't change the accuarcy, whereas increasing the pooling size to 3x3 lead to a worse accuarcy of ≈5%. Hence, no changes to the model were made.


# Number of units in single hidden layer
- increase from 128 to 256 units: worse accuracy (≈5%): 

# Number of hidden layers
Increasing the number of hidden layers to 2 didn't improve the accuarcy. A neural network with three layers even perfomed worse. Hence, no hidden layers were added.
- 2 layers of 128 units: slight increase in accuracy (≈95%)
- slightly worse accuarcy (≈90%) using three layers of 64 units

# Dropout rate
- 0.4: slightly worse accuracy of 92%
- 0.6: slightly worse accuarcy of 91%
