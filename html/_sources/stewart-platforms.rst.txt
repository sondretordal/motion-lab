.. _stewart-platforms:

Stewart Platforms
#################

Kinematics
==========


The orientation and position of the Stewart platforms are given as:

.. math::
    \bm{p}^n_{b/n} = 
    \begin{bmatrix}
    x \\ 
    y \\
    z
    \end{bmatrix} \in \mathbb{R}^3
    \hspace{10mm}
    \bm{\Theta}_{nb} =
    \begin{bmatrix}
    \phi \\
    \theta \\
    \psi
    \end{bmatrix} \in SO(3)
    
where the notation used :math:`\bm{p}^n_{b/n}` is the position of the Stewart platform's body frame :math:`\{b\}` relative to the inertal frame :math:`\{n\}`, given in the inertial frame :math:`\{n\}`. The velocites and accelerations share the same notation and are defined as:

.. math::
    \bm{v}^b_{b/n} =
    \begin{bmatrix}
    u \\
    v \\
    w
    \end{bmatrix} \in \mathbb{R}^3
    \hspace{10mm}
    \bm{\omega}^b_{b/n} =
    \begin{bmatrix}
    p \\
    q \\
    r
    \end{bmatrix} \in \mathbb{R}^3

The Euler angle sequence is defined by conventional rotation matrices. The explicit rotation sequence is given as:

.. math::
    \bm{R}^n_b(\bm{\Theta}_{nb}) = \bm{R}_x(\phi)\bm{R}_y(\theta)\bm{R}_z(\psi)
    \hspace{5mm} \text{or} \hspace{5mm}
    \bm{R}_z(\psi)\bm{R}_y(\theta)\bm{R}_x(\phi)

The accompanying transformation between time derivatives of the Euler angles :math:`\dot{\bm{\Theta}}_{nb}` and the local body-fixed rotational velocities :math:`\bm{\omega}^b_{b/n}` is given by the following two equations:

.. math::
    \dot{\bm{\Theta}}_{nb} = \bm{T}_\Theta(\bm{\Theta}_{nb})\bm{\omega}^b_{b/n}

.. math::
    \bm{\omega}^b_{b/n} =
    (\bm{R}_x(\phi)\bm{R}_y(\theta)\bm{R}_z(\psi))^T
    \begin{bmatrix}
    \dot{\phi} \\ 0 \\ 0
    \end{bmatrix}
    + (\bm{R}_y(\theta)\bm{R}_z(\psi))^T
    \begin{bmatrix}
    0 \\ \dot{\theta} \\ 0
    \end{bmatrix}
    + 
    \begin{bmatrix}
    0 \\ 0 \\ \dot{\psi}
    \end{bmatrix} \\

.. math::
    \underbrace{
    \left[ \begin {array}{ccc} \cos \left( \psi \right) \cos \left( 
    \theta \right) &-\sin \left( \psi \right) \cos \left( \theta \right) &
    \sin \left( \theta \right) \\ \noalign{\medskip}\cos \left( \psi
    \right) \sin \left( \theta \right) \sin \left( \phi \right) +\sin
    \left( \psi \right) \cos \left( \phi \right) &-\sin \left( \psi
    \right) \sin \left( \theta \right) \sin \left( \phi \right) +\cos
    \left( \psi \right) \cos \left( \phi \right) &-\cos \left( \theta
    \right) \sin \left( \phi \right) \\ \noalign{\medskip}-\cos \left( 
    \psi \right) \sin \left( \theta \right) \cos \left( \phi \right) +\sin
    \left( \psi \right) \sin \left( \phi \right) &\sin \left( \psi
    \right) \sin \left( \theta \right) \cos \left( \phi \right) +\cos
    \left( \psi \right) \sin \left( \phi \right) &\cos \left( \theta
    \right) \cos \left( \phi \right) \end {array} \right]
    }_{\bm{R}_{xyz}}



The feedback signals accessible as described in the :ref:`remote-io-interface`.