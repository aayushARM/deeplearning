import numpy as np


def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
  examples, where each example x[i] has shape (d_1, ..., d_k). We will
  reshape each input into a vector of dimension D = d_1 * ... * d_k, and
  then transform it to an output vector of dimension M.

  Inputs:
  - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
  - w: A numpy array of weights, of shape (D, M)
  - b: A numpy array of biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """
  out = None

  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  input_shape = x.shape[1:]
  num_inputs = x.shape[0]
  d_size = np.prod(input_shape)
  x_reshape = x.reshape(num_inputs, d_size)
  out = np.dot(x_reshape, w) + b

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  #kapild: loss is nothing but dL/dU= where dL/dy * dy/da * da/du = dout * da/du
  #############################################################################
  # Loss function calculation
  #############################################################################
  #  dL/dw= 
  #  where dL/dy * dy/da * da/dw 
  #  = dout * da/dw
  #
  #  da/dw = np.dot(X,W)/dw 
  #  which is X
  #############################################################################

  num_inputs = x.shape[0]
  num_d = x.shape[1:]
  num_layers = dout.shape[1]
  dw = np.dot(x.T, dout)
  dw = dw.T.reshape(num_layers, np.prod(num_d)).T
  #(6,5) (3,2,5)
  
  # db is the same np.dot(x.t, dout) but for b, x = 1 hence it comes out to be as
  db = np.sum(dout, axis=0)
  dx = np.dot(dout, w.T).reshape(num_inputs, *num_d)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  out = np.maximum(x,0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  dx = dout
  dx[x <=0] = 0
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


# def batchnorm_forward(x, gamma, beta, bn_param):
#   """
#   Forward pass for batch normalization.
  
#   During training the sample mean and (uncorrected) sample variance are
#   computed from minibatch statistics and used to normalize the incoming data.
#   During training we also keep an exponentially decaying running mean of the mean
#   and variance of each feature, and these averages are used to normalize data
#   at test-time.

#   At each timestep we update the running averages for mean and variance using
#   an exponential decay based on the momentum parameter:

#   running_mean = momentum * running_mean + (1 - momentum) * sample_mean
#   running_var = momentum * running_var + (1 - momentum) * sample_var

#   Note that the batch normalization paper suggests a different test-time
#   behavior: they compute sample mean and variance for each feature using a
#   large number of training images rather than using a running average. For
#   this implementation we have chosen to use running averages instead since
#   they do not require an additional estimation step; the torch7 implementation
#   of batch normalization also uses running averages.

#   Input:
#   - x: Data of shape (N, D)
#   - gamma: Scale parameter of shape (D,)
#   - beta: Shift paremeter of shape (D,)
#   - bn_param: Dictionary with the following keys:
#     - mode: 'train' or 'test'; required
#     - eps: Constant for numeric stability
#     - momentum: Constant for running mean / variance.
#     - running_mean: Array of shape (D,) giving running mean of features
#     - running_var Array of shape (D,) giving running variance of features

#   Returns a tuple of:
#   - out: of shape (N, D)
#   - cache: A tuple of values needed in the backward pass
#   """
#   mode = bn_param['mode']
#   eps = bn_param.get('eps', 1e-5)
#   momentum = bn_param.get('momentum', 0.9)

#   N, D = x.shape
#   running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
#   running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

#   out, cache, x_norm = None, None, None
#   if mode == 'train':
#     #############################################################################
#     # TODO: Implement the training-time forward pass for batch normalization.   #
#     # Use minibatch statistics to compute the mean and variance, use these      #
#     # statistics to normalize the incoming data, and scale and shift the        #
#     # normalized data using gamma and beta.                                     #
#     #                                                                           #
#     # You should store the output in the variable out. Any intermediates that   #
#     # you need for the backward pass should be stored in the cache variable.    #
#     #                                                                           #
#     # You should also use your computed sample mean and variance together with  #
#     # the momentum variable to update the running mean and running variance,    #
#     # storing your result in the running_mean and running_var variables.        #
#     #############################################################################
#     # import pdb
#     # pdb.set_trace()
#     batch_mean = np.mean(x, axis = 0)
#     batch_variance = np.var(x, axis = 0)

#     x_norm = (x - batch_mean)/np.sqrt(batch_variance + eps)
#     batch_variance_p_eps  =  batch_variance + eps
#     out = gamma * x_norm  + beta
    
#     running_mean = momentum * running_mean + (1 - momentum) * batch_mean
#     running_var  = momentum * running_var  + (1 - momentum) * batch_variance
#     #############################################################################
#     #                             END OF YOUR CODE                              #
#     #############################################################################
#   elif mode == 'test':
#     #############################################################################
#     # TODO: Implement the test-time forward pass for batch normalization. Use   #
#     # the running mean and variance to normalize the incoming data, then scale  #
#     # and shift the normalized data using gamma and beta. Store the result in   #
#     # the out variable.                                                         #
#     #############################################################################
#     batch_variance = running_var
#     batch_mean = running_mean
#     x_norm =  (x - running_mean)/np.sqrt(running_var + eps)
#     out = gamma * x_norm + beta
#     #############################################################################
#     #                             END OF YOUR CODE                              #
#     #############################################################################
#   else:
#     raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

#   # Store the updated running means back into bn_param
#   bn_param['running_mean'] = running_mean
#   bn_param['running_var'] = running_var

#   return out, cache


# def batchnorm_backward(dout, cache):
#   """
#   Backward pass for batch normalization.
  
#   For this implementation, you should write out a computation graph for
#   batch normalization on paper and propagate gradients backward through
#   intermediate nodes.
  
#   Inputs:
#   - dout: Upstream derivatives, of shape (N, D)
#   - cache: Variable of intermediates from batchnorm_forward.
  
#   Returns a tuple of:
#   - dx: Gradient with respect to inputs x, of shape (N, D)
#   - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
#   - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
#   """
#   dx, dgamma, dbeta = None, None, None
#   #############################################################################
#   # TODO: Implement the backward pass for batch normalization. Store the      #
#   # results in the dx, dgamma, and dbeta variables.                           #
#   #############################################################################
#   running_mean, running_var, x_norm, gamma, beta, batch_variance_p_eps, x, batch_mean = cache

#   dgamma = np.sum(x_norm *dout, axis = 0)
#   dbeta = np.sum(dout, axis = 0)

#   dh = dout * gamma

#   N = dout.shape[0]

#   dx = (1. / N) * gamma * (batch_variance_p_eps)**(-1. / 2.) * (N * dout - np.sum(dout, axis=0)
#     - (x - batch_mean) * (batch_variance_p_eps)**(-1.0) * np.sum(dout * (x - batch_mean ), axis=0))
  
#   #############################################################################
#   #                             END OF YOUR CODE                              #
#   #############################################################################

#   return dx, dgamma, dbeta

def batchnorm_forward(x, gamma, beta, bn_param):
  """
  Forward pass for batch normalization.
  
  During training the sample mean and (uncorrected) sample variance are
  computed from minibatch statistics and used to normalize the incoming data.
  During training we also keep an exponentially decaying running mean of the mean
  and variance of each feature, and these averages are used to normalize data
  at test-time.
  At each timestep we update the running averages for mean and variance using
  an exponential decay based on the momentum parameter:
  running_mean = momentum * running_mean + (1 - momentum) * sample_mean
  running_var = momentum * running_var + (1 - momentum) * sample_var
  Note that the batch normalization paper suggests a different test-time
  behavior: they compute sample mean and variance for each feature using a
  large number of training images rather than using a running average. For
  this implementation we have chosen to use running averages instead since
  they do not require an additional estimation step; the torch7 implementation
  of batch normalization also uses running averages.
  Input:
  - x: Data of shape (N, D)
  - gamma: Scale parameter of shape (D,)
  - beta: Shift paremeter of shape (D,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
  Returns a tuple of:
  - out: of shape (N, D)
  - cache: A tuple of values needed in the backward pass
  """
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, D = x.shape
  running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
  running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

  out, cache = None, None
  if mode == 'train':
    #############################################################################
    # TODO: Implement the training-time forward pass for batch normalization.   #
    # Use minibatch statistics to compute the mean and variance, use these      #
    # statistics to normalize the incoming data, and scale and shift the        #
    # normalized data using gamma and beta.                                     #
    #                                                                           #
    # You should store the output in the variable out. Any intermediates that   #
    # you need for the backward pass should be stored in the cache variable.    #
    #                                                                           #
    # You should also use your computed sample mean and variance together with  #
    # the momentum variable to update the running mean and running variance,    #
    # storing your result in the running_mean and running_var variables.        #
    #############################################################################
    sample_mean = np.mean(x, axis = 0) 
    sample_var = np.var(x, axis = 0)

    x_normalized = (x-sample_mean) / np.sqrt(sample_var + eps)
    out = gamma*x_normalized + beta


    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var


    cache = (x, sample_mean, sample_var, x_normalized, beta, gamma, eps)
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  elif mode == 'test':
    #############################################################################
    # TODO: Implement the test-time forward pass for batch normalization. Use   #
    # the running mean and variance to normalize the incoming data, then scale  #
    # and shift the normalized data using gamma and beta. Store the result in   #
    # the out variable.                                                         #
    #############################################################################
    x_normalized = (x - running_mean)/np.sqrt(running_var +eps)
    out = gamma*x_normalized + beta
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  # Store the updated running means back into bn_param
  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var

  return out, cache


def batchnorm_backward(dout, cache):
  """
  Backward pass for batch normalization.
  
  For this implementation, you should write out a computation graph for
  batch normalization on paper and propagate gradients backward through
  intermediate nodes.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, D)
  - cache: Variable of intermediates from batchnorm_forward.
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs x, of shape (N, D)
  - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
  - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #############################################################################
  
  (x, sample_mean, sample_var, x_normalized, beta, gamma, eps) = cache
  N = x.shape[0]
  dbeta = np.sum(dout, axis=0)
  dgamma = np.sum(x_normalized*dout, axis = 0)
  dx_normalized = gamma* dout
  dsample_var = np.sum(-1.0/2*dx_normalized*(x-sample_mean)/(sample_var+eps)**(3.0/2), axis =0)
  dsample_mean = np.sum(-1/np.sqrt(sample_var+eps)* dx_normalized, axis = 0) + 1.0/N*dsample_var *np.sum(-2*(x-sample_mean), axis = 0) 
  dx = 1/np.sqrt(sample_var+eps)*dx_normalized + dsample_var*2.0/N*(x-sample_mean) + 1.0/N*dsample_mean

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta

def batchnorm_backward_alt(dout, cache):
  """
  Alternative backward pass for batch normalization.
  
  For this implementation you should work out the derivatives for the batch
  normalizaton backward pass on paper and simplify as much as possible. You
  should be able to derive a simple expression for the backward pass.
  
  Note: This implementation should expect to receive the same cache variable
  as batchnorm_backward, but might not use all of the values in the cache.
  
  Inputs / outputs: Same as batchnorm_backward
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #                                                                           #
  # After computing the gradient with respect to the centered inputs, you     #
  # should be able to compute gradients with respect to the inputs in a       #
  # single statement; our implementation fits on a single 80-character line.  #
  #############################################################################
  running_mean, running_var, x_norm, gamma, beta, batch_variance_p_eps, x, batch_mean = cache

  dgamma = np.sum(x_norm *dout, axis = 0)
  dbeta = np.sum(dout, axis = 0)

  dh = dout * gamma

  N = dout.shape[0]

  dx = (1. / N) * gamma * (batch_variance_p_eps)**(-1. / 2.) * (N * dout - np.sum(dout, axis=0)
    - (x - batch_mean) * (batch_variance_p_eps)**(-1.0) * np.sum(dout * (x - batch_mean ), axis=0))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
  """
  Performs the forward pass for (inverted) dropout.

  Inputs:
  - x: Input data, of any shape
  - dropout_param: A dictionary with the following keys:
    - p: Dropout parameter. We drop each neuron output with probability p.
    - mode: 'test' or 'train'. If the mode is train, then perform dropout;
      if the mode is test, then just return the input.
    - seed: Seed for the random number generator. Passing seed makes this
      function deterministic, which is needed for gradient checking but not in
      real networks.

  Outputs:
  - out: Array of the same shape as x.
  - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
    mask that was used to multiply the input; in test mode, mask is None.
  """
  p, mode = dropout_param['p'], dropout_param['mode']
  if 'seed' in dropout_param:
    np.random.seed(dropout_param['seed'])

  mask = None
  out = None

  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase forward pass for inverted dropout.   #
    # Store the dropout mask in the mask variable.                            #
    ###########################################################################
    mask = (np.random.rand(*x.shape) < (1-p) )/(1-p)
    # element wise mulitiplication
    out = x * mask
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    ###########################################################################
    # TODO: Implement the test phase forward pass for inverted dropout.       #
    ###########################################################################
    out = x
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

  cache = (dropout_param, mask)
  out = out.astype(x.dtype, copy=False)

  return out, cache


def dropout_backward(dout, cache):
  """
  Perform the backward pass for (inverted) dropout.

  Inputs:
  - dout: Upstream derivatives, of any shape
  - cache: (dropout_param, mask) from dropout_forward.
  """
  dropout_param, mask = cache
  mode = dropout_param['mode']
  
  dx = None
  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase backward pass for inverted dropout.  #
    ###########################################################################
    dx = dout * mask
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    dx = dout
  return dx


def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
  out = None
  import pdb
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  wkd = w
  bkd = b
  # init some parameters
  N, C, H, W  = x.shape[0], x.shape[1], x.shape[2], x.shape[3]
  F, C1, HH, WW = w.shape[0], w.shape[1], w.shape[2], w.shape[3]
  bshape = b.shape[0]
  assert C == C1
  assert bshape == F
  pad = conv_param.get("pad")
  stride = conv_param.get("stride")
  h_filter_size = 1 + (H + 2 * pad - HH) / stride
  w_filter_size = 1 + (W + 2 * pad - WW) / stride

  #############################################################################
  #     pad the image first
  #############################################################################
  x_padded = []
  for n_index in range(N):
    image_x = x[n_index]
    pad_array = []
    pad_array.append((0,0))
    for channel_index in range(1, C):
      pad_array.append((pad, pad))
    image_x_pad = np.pad(image_x, pad_array, 'constant', constant_values=0)
    x_padded.append(image_x_pad)

  out = []
  for n_index in range(N):
    x_image = x_padded[n_index]
    rows, cols  = x_image.shape[1], x_image.shape[2]
    # print rows, cols
    for filter_index in range(F):
      w_filter = w[filter_index]
      b_filter = b[filter_index]
      filter_conv = []
      for row_index in xrange(0, rows - HH + 1, stride):
        for col_index in xrange(0, cols - WW + 1, stride):
          conv_image = x_image[:, row_index: HH + row_index, col_index: WW + col_index]
          # print "filter_index:%d, row_index:%d, col_index:%d" % (filter_index, row_index, col_index)
          # print "n_index:%d, w_filter.shape:%s, conv_image.shape:%s" % (n_index, w_filter.shape, conv_image.shape)
          shape_1 = np.prod(w_filter.shape)
          shape_2 = np.prod(conv_image.shape)
          assert shape_2 == shape_1
          ff = w_filter.reshape(shape_1)
          cc = conv_image.reshape(shape_1)  
          conv_dot = cc.dot(ff) + b_filter
          out.append(conv_dot)
  out = np.array(out).reshape((N, F, h_filter_size, w_filter_size))
  

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b, conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  # """
  # dx, dw, db = None, None, None
  # #############################################################################
  # # TODO: Implement the convolutional backward pass.                          #
  # #############################################################################
  x, w, b, conv_param = cache

  N, C, H, W  = x.shape[0], x.shape[1], x.shape[2], x.shape[3]
  F, C1, HH, WW = w.shape[0], w.shape[1], w.shape[2], w.shape[3]
  bshape = b.shape[0]
  assert C == C1
  assert bshape == F
  pad = conv_param.get("pad")
  stride = conv_param.get("stride")
  h_filter_size = 1 + (H + 2 * pad - HH) / stride
  w_filter_size = 1 + (W + 2 * pad - WW) / stride

  # #############################################################################
  # #     pad the image first and dout so that they are are easy to process.
  # #############################################################################
  x_padded = []
  for n_index in range(N):
    image_x = x[n_index]
    pad_array = []
    pad_array.append((0,0))
    for channel_index in range(1, C):
      pad_array.append((pad, pad))
    image_x_pad = np.pad(image_x, pad_array, 'constant', constant_values=0)
    x_padded.append(image_x_pad)

  x_padded = np.array(x_padded)
  #############################################################################
  #     compute the error loss.
  #############################################################################

  import pdb
  dx = np.array(len(x_padded) * [np.zeros(x_padded[0].shape)])
  dw = np.zeros((w.shape))
  db = np.zeros((b.shape))
  # Alternatively can use.
    # dx = np.zeros_like(x)
    # dw = np.zeros_like(w)
    # db = np.zeros_like(b)

  for n_index in range(N):
    rows, cols  = x_padded[0].shape[1], x_padded[0].shape[2]
    for filter_index in range(F):
      w_filter = w[filter_index]
      for row_index in xrange(0, rows - HH + 1, stride):
        for col_index in xrange(0, cols - WW + 1, stride):

          x_conv_image = x_padded[n_index, :, row_index: HH + row_index, col_index: WW + col_index]
          dout_padded_oj = dout[n_index, filter_index, row_index/stride, col_index/stride]
          dx[n_index, :, row_index: HH + row_index, col_index: WW + col_index] += w_filter * dout_padded_oj

          dw[filter_index] += x_conv_image * dout_padded_oj
          db[filter_index] += dout_padded_oj

  # unpad
  dx = dx[:, :, pad:-pad, pad:-pad]

  
  return dx, dw, db  

def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################

  # init variables
  N, C, H, W = x.shape[0], x.shape[1], x.shape[2], x.shape[3]
  height = pool_param.get("pool_height")
  width = pool_param.get("pool_width")
  stride = pool_param.get("stride")

  # for n in xrange(N):
  #   for c in xrange(C):
  #     for w in xrange(0, width):
  #       for h in xrange(height):

  h2 = (H - height)/stride + 1
  w2 = (W - width)/stride + 1

  out = np.zeros((N, C, h2, w2))
  out_argmax = np.zeros((N, C, h2, w2))
  # print out.shape
  for n in xrange(N):
    for c in xrange(C):
      for row_index in xrange(0, H - height + 1, stride):
        for col_index in xrange(0, W - width + 1, stride):
          pool_image = x[n, c, row_index : row_index + height, col_index : col_index + width]
          out[n, c, row_index/stride, col_index/stride] = np.max(pool_image)
          out_argmax[n, c, row_index/stride, col_index/stride] = np.argmax(pool_image)


  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, pool_param, out_argmax)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  x, pool_param, out_argmax = cache
  N, C, H, W = x.shape[0], x.shape[1], x.shape[2], x.shape[3]
  height = pool_param.get("pool_height")
  width = pool_param.get("pool_width")
  stride = pool_param.get("stride")

  dx = np.zeros_like(x)
  for n in xrange(N):
    for c in xrange(C):
      for row_index in xrange(0, H - height + 1, stride):
        for col_index in xrange(0, W - width + 1, stride):
          argmax_location = out_argmax[n, c, row_index/stride, col_index/stride]
          dout_i = dout[n, c, row_index/stride, col_index/stride]
          index = 0
          for i in range(0, height):
            for j in range(0, width):
              if (index == argmax_location):
                dx[n, c, row_index : row_index + height, col_index : col_index + width][i,j] +=  dout_i
              index += 1

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def spatial_batchnorm_forward_old(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """

  #############################################################################
  # TODO: Implement the forward pass for spatial batch normalization.         #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, C, H, W = x.shape

  total_features = np.prod((N, H, W))

  running_mean = bn_param.get('running_mean', np.zeros(C, dtype=x.dtype))
  running_var = bn_param.get('running_var', np.zeros(C, dtype=x.dtype))
  # x_normalized = np.zeros_like(x)
  out, cache = np.zeros_like(x), None
  if mode == 'train':
    for c in xrange(C):
      x_per_channel = x[:, c, :, :]
      prod_h_w = np.prod((x_per_channel.shape[0], x_per_channel.shape[1], x_per_channel.shape[2]))
      x_reshape = x_per_channel.reshape(prod_h_w, 1)
      sample_mean = np.mean(x_reshape, axis=(0)) 
      sample_var = np.var(x_reshape, axis=(0))
      x_normalized = (x_per_channel-sample_mean) / np.sqrt(sample_var + eps)
      out[:, c, :, :] = gamma[c]*x_normalized + beta[c]
      running_mean[c] = momentum * running_mean[c] + (1 - momentum) * sample_mean
      running_var[c] = momentum * running_var[c] + (1 - momentum) * sample_var

    cache = (x, sample_mean, sample_var, x_normalized, beta, gamma, eps)
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  elif mode == 'test':
    for c in xrange(C):
      x_per_channel = x[:, c, :, :]
      x_normalized_per_channel = (x_per_channel - running_mean[c]) / np.sqrt(running_var[c] + eps)
      out[:, c, :, :] = gamma[c] * x_normalized_per_channel + beta[c]
    batch_variance = running_var
    batch_mean = running_mean  
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  
  # Store the updated running means back into bn_param
  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var



  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return out, cache

def spatial_batchnorm_forward(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """

  #############################################################################
  # TODO: Implement the forward pass for spatial batch normalization.         #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, C, H, W = x.shape

  total_features = np.prod((N, H, W))
  flat_x = swap_and_reshape_axis(x, *x.shape)
  out_temp, cache = batchnorm_forward(flat_x, gamma, beta, bn_param)
  out = reshape_and_swap_axis(out_temp, *x.shape)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return out, cache


def swap_and_reshape_axis(X, N, C, H, W):
  x_swap = np.swapaxes(X, 0, 1)
  flat_x = x_swap.reshape(C, -1)
  return flat_x.T

def reshape_and_swap_axis(flat_x, N, C, H, W):
  x_reshaped = flat_x.T.reshape(C, N, H, W)
  x_swap = np.swapaxes(x_reshaped, 0, 1)
  return x_swap

def spatial_batchnorm_backward(dout, cache):
  """
  Computes the backward pass for spatial batch normalization.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, C, H, W)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs, of shape (N, C, H, W)
  - dgamma: Gradient with respect to scale parameter, of shape (C,)
  - dbeta: Gradient with respect to shift parameter, of shape (C,)
  """
  dx, dgamma, dbeta = None, None, None


  #############################################################################
  # TODO: Implement the backward pass for spatial batch normalization.        #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  # import pdb
  # pdb.set_trace()
  dout_temp = swap_and_reshape_axis(dout, *dout.shape)
  # import pdb
  # pdb.set_trace()
  dx_temp, dgamma, dbeta = batchnorm_backward(dout_temp, cache)
  dx = reshape_and_swap_axis(dx_temp, *dout.shape)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta
  

def svm_loss(x, y):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  N = x.shape[0]
  correct_class_scores = x[np.arange(N), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(N), y] = 0
  loss = np.sum(margins) / N
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(N), y] -= num_pos
  dx /= N
  return loss, dx


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  N = x.shape[0]
  loss = -np.sum(np.log(probs[np.arange(N), y])) / N
  dx = probs.copy()
  dx[np.arange(N), y] -= 1
  dx /= N
  return loss, dx
