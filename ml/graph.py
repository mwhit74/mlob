
def graph_shear_envelope(node_loc, V_max1, V_max2):
    """Plot shear envelope diagrams"""
    node_loc = node_loc[:(len(node_loc)/2+1)]
    plt.figure(1)
    plt.subplot(211)
    plt.plot(node_loc, V_max1)
    plt.subplot(212)
    plt.plot(node_loc, V_max2)
    plt.show()

def graph_moment_envelope(node_loc, M_max1, M_max2):
    """Plot moment envelope diagrams"""
    node_loc = node_loc[:(len(node_loc)/2+1)]
    plt.figure(1)
    plt.subplot(211)
    plt.plot(node_loc, M_max1)
    plt.subplot(212)
    plt.plot(node_loc, M_max2)
    plt.show()
