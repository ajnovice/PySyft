from crypten.mpc import MPCTensor
from crypten.mpc.ptype import ptype as Ptype

from syft.generic.frameworks.hook import hook_args
from syft.generic.tensor import AbstractTensor


class SyftCrypTensor(AbstractTensor):
    def __init__(
        self,
        owner=None,
        id=None,
        tensor: MPCTensor = None,
        tags: set = None,
        description: str = None,
    ):
        super().__init__(id=id, owner=owner, tags=tags, description=description)
        self.tensor = tensor

    def get_class_attributes(self):
        """
        Specify all the attributes need to build a wrapper correctly when returning a response,
        """
        return {"tensor": self.tensor}

    @property
    def data(self):
        return self

    @data.setter
    def data(self, new_data):
        self.child = new_data.child
        return self

    @staticmethod
    def new(*args, **kwargs):
        """
        Creates a new MPCTensor, passing all args and kwargs into the constructor.
        """
        return MPCTensor(*args, **kwargs)

    def from_shares(self, share, precision=None, src=0, ptype=Ptype.arithmetic):
        return self.tensor.from_share(share, precision=None, src=0, ptype=Ptype.arithmetic)

    def clone(self):
        return self.tensor.clone()

    def shallow_copy(self):
        return self.tensor.shallow_copy()

    def get_plain_text(self, dst=None):
        """Decrypts the tensor."""
        return self.tensor.get_plain_text(dst=dst)

    def to(self, ptype, **kwargs):
        """Converts self.tensor to the given ptype

           Args: ptype: Ptype.arithmetic or Ptype.binary"""
        self.tensor = self.tensor.to(ptype, **kwargs)
        return self

    def arithmetic(self):
        """Converts self.tensor to arithmetic secret sharing"""
        self.tensor = self.tensor.arithmetic()
        return self

    def binary(self):
        """Converts self.tensor to binary secret sharing"""
        self.tensor = self.tensor.binary()
        return self

    def reveal(self, dst=None):
        """Decrypts the tensor without any downscaling."""
        self.tensor = self.tensor.reveal(dst=dst)
        return self

    def __repr__(self):
        self.tensor.__repr__()

    def __setitem__(self, index, value):
        self.tensor.__setitem__(index, value)

    def get_share(self):
        return self.tensor.share()

    def set_share(self, value):
        self.tensor = value

    def get_encoder(self):
        return self.tensor.encoder()

    def set_encoder(self, value):
        self.tensor.encoder = value


### Register the tensor with hook_args.py ###
hook_args.default_register_tensor(SyftCrypTensor)
