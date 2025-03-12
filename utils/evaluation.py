import torch

def chamfer_loss(X,Y):
#     if Debug.keops and 4*X.shape[0]*X.shape[1]*Y.shape[1] > 1e8:
#         print('.')
#         lX = LazyTensor(X[:,None,:,:].contiguous())
#         lXt = LazyTensor(Y[:,:,None,:].contiguous())
#         Ds = ((lX-lXt)**2).sum(-1).sqrt()
#         losses = Ds.min(2).mean(-1) + Ds.min(1).mean(-1)
#     else:
    X = torch.tensor(X)
    Y = torch.tensor(Y)
    dist = torch.cdist(X,Y)
    losses = dist.min(-1)[0].mean(-1)+dist.min(-2)[0].mean(-1)
    return losses.numpy()

def chamfer_p2p(X,Y):
#     if Debug.keops and 4*X.shape[0]*X.shape[1]*Y.shape[1] > 1e8:
#         print('.')
#         lX = LazyTensor(X[:,None,:,:].contiguous())
#         lXt = LazyTensor(Y[:,:,None,:].contiguous())
#         Ds = ((lX-lXt)**2).sum(-1).sqrt()
#         losses = Ds.min(2).mean(-1) + Ds.min(1).mean(-1)
#     else:
    X = torch.tensor(X)
    Y = torch.tensor(Y)
    dist = torch.cdist(X,Y)
    losses = dist.min(-1)[0]
    return losses.numpy()