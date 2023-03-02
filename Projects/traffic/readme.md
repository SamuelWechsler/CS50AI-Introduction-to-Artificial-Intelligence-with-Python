# Increasing repetitions of convolution and pooling
Repeating 2D-convolution and max-pooling at least twice lead to a substantial increase
in accuarcy estimated on the test set (≈95%) whereas performing convolution and pooling once was associated with a poor accuarcy (≈5%).

# Pooling size, size of convolutional filter
- increase in conv filters: no increase in accuarcy
- increase in pooling size: decrease in accuracy

# Number of hidden layers
- no increase in accuracy with second hidden layer of 64 units
- worse accuarcy using three layers of 64 units
