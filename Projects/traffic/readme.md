# Increasing repetitions of convolution and pooling
Repeating 2D-convolution and max-pooling at least twice lead to a substantial increase in accuarcy estimated on the test set (≈95%) whereas performing convolution and pooling once was associated with a poor accuarcy (≈5%).

Summary of the model so far:
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
_________________________________________________________________
 conv2d (Conv2D)             (None, 28, 28, 32)        1792      
                                                                 
 max_pooling2d (MaxPooling2D  (None, 14, 14, 32)       0         
 )                                                               
                                                                 
 conv2d_1 (Conv2D)           (None, 12, 12, 32)        18464     
                                                                 
 max_pooling2d_1 (MaxPooling  (None, 6, 6, 32)         0         
 2D)                                                             
                                                                 
 flatten (Flatten)           (None, 1152)              0         
                                                                 
 dense (Dense)               (None, 128)               147584    
                                                                 
 dropout (Dropout)           (None, 128)               0         
                                                                 
 dense_1 (Dense)             (None, 43)                5547      
                                                                 
_________________________________________________________________
Total params: 173,387
Trainable params: 173,387
Non-trainable params: 0
_________________________________________________________________

# Pooling size, size of convolutional filter
The number of convolutional filters and the size of the pooling matrix seems to optimal at 32 filters and 2x2. Increasing the number of convolutional filters didn't change the accuarcy, whereas increasing the pooling size to 3x3 lead to a worse accuarcy of ≈5%. Hence, no changes to the model were made.


# Number of units in single hidden layer
- increase from 128 to 256 units: worse accuracy (≈5%): 

# Number of hidden layers
Increasing the number of hidden layers to 2 didn't improve the accuarcy. A neural network with three layers even perfomed worse. Hence, no hidden layers were added.
- 2 layers of 128 units: slight increase in accuracy (≈95%)
- slightly worse accuarcy (≈90%) using three layers of 64 units

Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
_________________________________________________________________
 conv2d (Conv2D)             (None, 28, 28, 32)        1792      
                                                                 
 max_pooling2d (MaxPooling2D  (None, 14, 14, 32)       0         
 )                                                               
                                                                 
 conv2d_1 (Conv2D)           (None, 12, 12, 32)        18464     
                                                                 
 max_pooling2d_1 (MaxPooling  (None, 6, 6, 32)         0         
 2D)                                                             
                                                                 
 flatten (Flatten)           (None, 1152)              0         
                                                                 
 dense (Dense)               (None, 64)                73792     
                                                                 
 dense_1 (Dense)             (None, 64)                4160      
                                                                 
 dense_2 (Dense)             (None, 64)                4160      
                                                                 
 dropout (Dropout)           (None, 64)                0         
                                                                 
 dense_3 (Dense)             (None, 43)                2795      
                                                                 
_________________________________________________________________
Total params: 105,163
Trainable params: 105,163
Non-trainable params: 0
_________________________________________________________________

# Dropout rate
- 0.4: slightly worse accuracy of 92%
- 0.6: slightly worse accuarcy of 91%

# Further Experimentation with Convolution