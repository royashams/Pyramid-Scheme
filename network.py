# The following helper function was taken from Lab06.
def gather_lists(list_):
    """
    Return the concatenation of the sub lists of list_.

    :param list_: list of sub lists
    :type list_: list[list]
    :rtype: list

    >>> list_ = [[1, 2], [3, 4]]
    >>> gather_lists(list_)
    [1, 2, 3, 4]
    """
    # this is a case where list comprehension gets a bit unreadable
    new_list = []
    for sub in list_:
        for element in sub:
            new_list.append(element)
    return new_list


class Network(object):
    """A pyramid network.

    This class represents a pyramid network. The network topology can be loaded
    from a file, and it can find the best arrest scenario to maximize the seized
    asset.

    You may, if you wish, change the API of this class to add extra public
    methods or attributes. Make sure that you do not change the public methods
    that were defined in the handout. Otherwise, you may fail test results for
    those methods.

    """

    # === Attributes ===
    # :type data: None|Tuple
    #     A tuple containing the information of a member node, organized by
    #     name,(str) then their assets.
    # :type children_: None|List
    #     A list of Network nodes that contain the children of a member node.
    # :type sponsor_: None|Network
    #     The sponsor node of a member node. This is None if the member node is
    #     the "Great Boss"
    # :type mentor_: None|Network
    #     The mentor node of a member node. This is None if the member node is
    #     the "Great Boss", the Sponsor node if the member is the first child of
    #     the sponsor, or the child preceding the addition of the member node.

    def __init__(self, data=None, children_=None, sponsor_=None, mentor_=None):
        """
        Create and initialize this Network self.

        :rtype: None
        """

        self.data = data
        self.sponsor_ = sponsor_
        self.mentor_ = mentor_
        # copy children_ if not None
        self.children_ = children_.copy() if children_ else []
        # similar to the tree structure discussed in class.

    def name_lookup(self, name):
        """
        A helper function that returns a list of the network node given a
        member's name.

        :type name: str
            The name of the member who is looked up
        :rtype: List of Network

        >>> n1 = Network(('Emma', 32))
        >>> n2 = Network(('Liam', 20), [n1])
        >>> n2
        Network(('Liam', 20), [Network(('Emma', 32))])
        >>> n1
        Network(('Emma', 32))
        >>> n2.children_
        [Network(('Emma', 32))]
        >>> n2.data
        ('Liam', 20)
        >>> n2.name_lookup('Emma')
        [Network(('Emma', 32))]
        >>> n2.name_lookup('Liam')
        [Network(('Liam', 20), [Network(('Emma', 32))])]

        """
        if self.data[0] == name:
            return [self]
        else:
            return gather_lists([x.name_lookup(name) for x in self.children_])

    def __add__(self, other):
        """
        A helper function that adds a member to the Network.

        :type other: Tuple
            This is a tuple containing other's data, children_, and sponsor_
        :rtype: None

        >>> n1 = Network()
        >>> n1.__add__(('Liam', 20))
        >>> n1
        Network(('Liam', 20))
        >>> n1.__add__((('Emma', 32), None, 'Liam'))
        >>> n1
        Network(('Liam', 20), [Network(('Emma', 32))])
        >>> n1.children_
        [Network(('Emma', 32))]
        >>> n1.children_[0].sponsor_
        Network(('Liam', 20), [Network(('Emma', 32))])
        >>> n1.__add__((('Mason', 14), None, 'Emma'))
        >>> n1
        Network(('Liam', 20), [Network(('Emma', 32), [Network(('Mason', 14))])])
        >>> mason = n1.name_lookup('Mason')
        >>> mason[0].sponsor_.data
        ('Emma', 32)
        >>> mason[0].mentor_.data
        ('Emma', 32)
        >>> n1.__add__((('Olivia', 8), None, 'Emma'))
        >>> olivia = n1.name_lookup('Olivia')
        >>> olivia[0].sponsor_.data
        ('Emma', 32)
        >>> olivia[0].mentor_.data
        ('Mason', 14)

        """
        if self.data is None:
            # empty network
            self.data = other
        else:
            new = Network(other[0], other[1], other[2])
            # create a new network out of the member added
            new_sponsor_ = other[2]
            # now search for the sponsor_ and make children_
            sponsor_node = self.name_lookup(new_sponsor_)[0]
            # because name_lookup returns a list, this is just indexing for
            # the node
            sponsor_node.children_.append(new)
            # add the new member to the sponsor_'s children_
            new.sponsor_ = sponsor_node

            # Now its time to change the mentor node.
            sponsor_children = sponsor_node.children_
            # create a list of the sponsor's children_.
            position = sponsor_children.index(new)
            if position == 0:
                # if the member is the first child in list, return the
                # sponsor's node
                new.mentor_ = new.sponsor_
            else:
                # if not first child, return the child before the occurrence
                # of member
                child_before = sponsor_children[position - 1]
                new.mentor_ = child_before

    def __repr__(self):
        """
        Return representation of Network (self) as string that
        can be evaluated into an equivalent Network.

        :rtype: str

        >>> n1 = Network()
        >>> n1
        Network(None)
        >>> n2 = Network(('Finn', 20))
        >>> n2
        Network(('Finn', 20))
        >>> n3 = Network(('Name', 40), [n2])
        >>> n3
        Network(('Name', 40), [Network(('Finn', 20))])

        """
        # the __repr__ is very similar to the one written in tree.py as
        # discussed in lecture.
        return ('Network({}, {})'.format(repr(self.data), repr(self.children_))
                if self.children_
                else 'Network({})'.format(repr(self.data)))

    def __str__(self, indent=0):
        """
        Return a user-friendly string representation of Network(self)

        :rtype: str

        >>> n1 = Network()
        >>> n1.__add__(('Liam', 20))
        >>> n1.__add__((('Emma', 32), None, 'Liam'))
        >>> n1.__add__((('Mason', 14), None, 'Emma'))
        >>> n1.__add__((('Finn', 706), None, 'Emma'))
        >>> n1.__add__((('Jake', 0), [Network(('lol', 2))], 'Liam'))
        >>> print(n1)
        ('Liam', 20)
           ('Emma', 32)
              ('Mason', 14)
              ('Finn', 706)
           ('Jake', 0)
              ('lol', 2)
        >>> lol = n1.name_lookup('Finn')
        >>> lol[0]
        Network(('Finn', 706))
        >>> lol[0].sponsor_.data
        ('Emma', 32)

        """
        # the __str__ is very similar to the one written in tree.py as
        # discussed in lecture.
        boss_str = indent * " " + str(self.data)
        return '\n'.join([boss_str] +
                         [c.__str__(indent + 3) for c in self.children_])

    def load_log(self, log_file_name):
        """
        Load the network topology from the log log_file_name.

        :type log_file_name: str
            Name of the log file that creates the topology
        :rtype: None

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> print(n1)
        ('Liam', 20)
           ('Emma', 32)
              ('Mason', 14)
              ('Sophia', 5)
              ('Olivia', 8)
           ('Jacob', 50)
              ('William', 42)
                 ('James', 10)
                    ('Alexander', 60)
              ('Ethan', 5)

        >>> jacob = n1.name_lookup('Jacob')
        >>> jacob[0].sponsor_.data
        ('Liam', 20)

        """
        log_file = open(log_file_name)

        for current_line in log_file:
            stripped_line = current_line.strip()
            new_member = stripped_line.split('#')
            # this creates a node with the member's name and asset.
            member_data = (new_member[0], int(new_member[-1]))
            if len(new_member) == 3:
                # member has a sponsor_
                new_sponsor_ = new_member[1]
                member_tuple = (member_data, None, new_sponsor_)
                self.__add__(member_tuple)
            elif len(new_member) == 2:
                # member is the great boss/ no sponsor_
                member_tuple = member_data
                self.__add__(member_tuple)

    def sponsor(self, member_name):
        """
        Return the sponsor name of member with name member_name.

        :type member_name: str
            This is a member's name from the network
        :rtype: str

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> n1.sponsor("William")
        'Jacob'
        >>> print(n1.sponsor("Liam"))
        None
        """
        member_node = self.name_lookup(member_name)
        # retrieve the node of the member in the argument
        if len(member_node) != 0:
            if member_node[0].sponsor_:
                return member_node[0].sponsor_.data[0]
            else:
                return str(None)
        else:
            pass

    def mentor(self, member_name):
        """
        Return the mentor name of member with name member_name.

        :type member_name: str
            name of the member whose mentor is to be found
        :rtype: str

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> n1.mentor("Emma")
        'Liam'
        >>> n1.mentor("Mason")
        'Emma'
        >>> n1.mentor("Sophia")
        'Mason'
        >>> n1.mentor("Olivia")
        'Sophia'
        >>> n1.mentor("James")
        'William'
        >>> print(n1.mentor("Liam"))
        None
        >>> print(n1)
        ('Liam', 20)
           ('Emma', 32)
              ('Mason', 14)
              ('Sophia', 5)
              ('Olivia', 8)
           ('Jacob', 50)
              ('William', 42)
                 ('James', 10)
                    ('Alexander', 60)
              ('Ethan', 5)

        """
        member_node = self.name_lookup(member_name)
        # retrieve the node of the member in the argument
        if member_node[0].mentor_:
            return member_node[0].mentor_.data[0]
        else:
            return str(None)

    def assets(self, member_name):
        """
        Return the assets of member with name member_name.

        :type member_name: str
            This is a member's name from the network
        :rtype: int

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> n1.assets('Liam')
        20
        >>> n1.assets('Alexander')
        60
        >>> n1.assets('Jacob')
        50
        """
        member_node = self.name_lookup(member_name)
        return member_node[0].data[1]

    def children(self, member_name):
        """Return the name of all children of member with name member_name.

        :type member_name: str
            This is a member's name from the network
        :rtype: list

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> n1.children('Liam')
        ['Emma', 'Jacob']
        >>> n1.children("Emma")
        ['Mason', 'Sophia', 'Olivia']
        """
        member_node = self.name_lookup(member_name)
        # retrieve the node of the member in the argument
        if member_node[0].children_:
            return [x.data[0] for x in member_node[0].children_]
        else:
            # if there are no children
            return []

        # more helper functions

    def list_relative_nodes(self, member_name):
        """
        A helper function that returns a list of nodes that are related to
        member_name's node. Relatives include the sponsor, mentor, and children.
        This list has no duplicate nodes listed.

        :type member_name: str
            This is a member's name from the network.
        :rtype: List of Network

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> liam_rel =  n1.list_relative_nodes('Liam')
        >>> names = [node.data[0] for node in liam_rel]
        >>> names
        ['Emma', 'Jacob']
        >>> emma_rel = n1.list_relative_nodes('Emma')
        >>> names = [node.data[0] for node in emma_rel]
        >>> names
        ['Liam', 'Mason', 'Sophia', 'Olivia']
        >>> ethan_rel = n1.list_relative_nodes('Ethan')
        >>> names = [node.data[0] for node in ethan_rel]
        >>> names
        ['Jacob', 'William']
        >>> alex_rel = n1.list_relative_nodes('Alexander')
        >>> names = [node.data[0] for node in alex_rel]
        >>> names
        ['James']

        """
        member = self.name_lookup(member_name)
        if len(member) == 0:
            relative_list = []
        else:
            member_node = member[0]
            relative_list = []
            if member_node.sponsor_:
                relative_list.append(member_node.sponsor_)
            if member_node.mentor_:
                if member_node.mentor_ != member_node.sponsor_:
                    # there may be a case where the mentor is the same
                    # as sponsor
                    relative_list.append(member_node.mentor_)
            if len(member_node.children_) != 0:
                # checks if children are not empty
                for child in member_node.children_:
                    relative_list.append(child)
            else:
                pass

        return relative_list

    def one_asset(self, name, maximum_arrests):
        """
        A helper function which returns the best arrest seize for only one
        member (target zero) in the network. This function calls on the helper
        class FamilyTree.

        :type name: str
            name of member in Network.
        :rtype: int

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> n1.one_asset('Liam', 1)
        20
        >>> n1.one_asset('Alexander', 4)
        162
        """
        fam = FamilyTree()
        member_node = self.name_lookup(name)[0]
        # create a new FamilyTree instance
        fam.populate(self, member_node.data[0], maximum_arrests)
        arrest = fam.optimal_arrests()
        return arrest

    def name_list(self):
        """
        A helper function that returns a list of all the names in the network.

        :rtype: list of str

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> n1.name_list()[:5]
        ['Liam', 'Emma', 'Mason', 'Sophia', 'Olivia']
        >>> n1.name_list()[5:]
        ['Jacob', 'William', 'James', 'Alexander', 'Ethan']
        """
        if self.data:
            name = [self.data[0]]
            # recursively look for all names
        else:
            return []
        return gather_lists([name] + [x.name_list() for x in self.children_])

    def best_arrest_assets(self, maximum_arrest):
        """
        Search for the amount of seized assets in the best arrest scenario
        that maximizes the seized assets. Consider all members as target zero.

        :type maximum_arrest: int
            this is the maximum amount of arrests that generates a sum of money
        :rtype: int

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> n1.best_arrest_assets(1)
        60
        >>> n1.best_arrest_assets(2)
        92
        >>> n1.best_arrest_assets(4)
        162
        >>> n1.best_arrest_assets(8)
        233
        """
        names = self.name_list()
        optimal_arrest_list = []
        # make an empty list so we add all the optimal arrests onto it
        for x in names:
            optimal = self.one_asset(x, maximum_arrest)
            optimal_arrest_list.append(optimal)
        if len(optimal_arrest_list) > 0:
            return max(optimal_arrest_list)
        else:
            return 0

    def best_arrest_order(self, maximum_arrest):
        """
        Search for list of member names in the best arrest scenario that
        maximizes the seized assets. Consider all members as target zero,
        and the order in the list represents the order that members are
        arrested.

        :type maximum_arrest: int
            this is the maximum amount of arrests that generates a path of
            members in the network.
        :rtype: list of str

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> n1.best_arrest_order(1)
        ['Alexander']
        >>> n1.best_arrest_order(2)
        ['Jacob', 'William']
        >>> n1.best_arrest_order(4)
        ['Jacob', 'William', 'James', 'Alexander']
        >>> n1.best_arrest_order(8)[:7]
        ['Alexander', 'James', 'William', 'Jacob', 'Liam', 'Emma', 'Sophia']
        >>> n1.best_arrest_order(8)[7:]
        ['Mason']
        """
        names = self.name_list()
        path_list = []
        optimal_arrest_list = []
        for x in names:
            # create a list of all of the paths for each member
            fam = FamilyTree()
            fam.populate(self, x, maximum_arrest)
            arrests = fam.optimal_arrests()
            optimal = fam.optimal_path(arrests)
            path_list.append(optimal)

            # create a list of all of the optimal arrests for each member
            # this is similar to the best_arrest_assets function
            optimal = self.one_asset(x, maximum_arrest)
            optimal_arrest_list.append(optimal)

        best = self.best_arrest_assets(maximum_arrest)
        # find the position of 'best' in the list of all arrests, and use
        # its index for finding the path in path_list.

        if len(optimal_arrest_list) > 0:
            pos = optimal_arrest_list.index(best)
            # for i in range(len(names)):
            #     print((path_list)[i])
            best_path = path_list[pos]

            # remove duplicate strings if any, this is mostly for debugging
            # purposes.
            single_set = set()
            result = []
            for name in best_path:
                if name not in single_set:
                    single_set.add(name)
                    result.append(name)
            return result
        else:
            return []


# HELPER CLASS


class FamilyTree(object):
    """
    A Family Tree.

    This is a helper class with the objective of targeting a single member
    (target zero) and finding all possible paths of related members (sponsor,
    mentor, children). This class creates a tree-like data structure starting
    with "target zero" as the root, and branches out into other members.

    This class also keeps track of every member in a path from the root to leaf,
    and also keeps track of the total assets seized.

    # === Attributes ===
    # :type node: None|Network
    #     A Network node containing information about its data, sponsor,
    #     Mentor, and children.
    # :type relatives: None|List of FamilyTree
    #     A list of FamilyTree nodes that are related somehow to self. Any
    #     Sponsor, Mentor, or Child of the member is considered a relative.
    # :type seen: None|List of Str
    #     A list of member names for each path in the FamilyTree. This keeps
    #     track in each node of the sponsors up until the root node. Useful in
    #     determining best_arrest_order.
    # :type total: int
    #     A number recording the total assets seized for each path. This keeps
    #     a sum of assets from a node, to its sponsor, up until the root node.
    #     Useful in determining best_arrest_assets.

    """

    def __init__(self, node=None, relatives=None, seen=None, total=0):
        """
        Initialize this FamilyTree self.

        :type node: None | Network
            The Network node of a member to be added to the FamilyTree.
        :type relatives: list of Nodes

        :type seen: list of str
            A list of names that have already been seen in a path from the root
            to any member.
        :type total: int
            The total number of assets seized in a path from the root to any
            member.
        """
        self.node = node
        # this is like data but really its a network node
        self.relatives = relatives
        self.seen = seen
        self.total = total
        # copy children_ if not None
        self.relatives = relatives.copy() if relatives else []

    def __str__(self, indent=0):
        """
        Return a user-friendly string representation of Network(self)

        :rtype: str

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> f = FamilyTree()
        >>> f.__add__(n1, 'Ethan')
        >>> print(f)
        ('Ethan', 5) , ['Ethan'] , 5
        >>> f.__add__(n1, 'Jacob', 'Ethan')
        >>> f.__add__(n1, 'William', 'Ethan')
        >>> f.__add__(n1, 'James', 'William')
        >>> print(f)
        ('Ethan', 5) , ['Ethan'] , 5
           ('Jacob', 50) , ['Ethan', 'Jacob'] , 55
           ('William', 42) , ['Ethan', 'William'] , 47
              ('James', 10) , ['Ethan', 'William', 'James'] , 57
        """

        boss_str = indent * " " + str(self.node.data) + ' , ' + \
            str(self.seen) + ' , ' + str(self.total)
        return '\n'.join([boss_str] + [c.__str__(indent + 3) for c in
                                       self.relatives])

    def __repr__(self):
        """
        Return representation of FamilyTree (self) as string that
        can be evaluated into an equivalent FamilyTree.

        :rtype: str

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> ethan = n1.name_lookup('Ethan')[0]
        >>> em_rel = n1.list_relative_nodes('Ethan')
        >>> f = FamilyTree(ethan, em_rel)
        """
        # __repr__ is very similar to the one discussed in lecture from tree.py.
        return ('FamilyTree({}, {})'.format(repr(self.node.data[0]),
                                            repr(self.relatives))
                if self.relatives
                else 'FamilyTree({})'.format(repr(self.node)))

    def populate(self, network, name, maximum_arrests, parent=None, org=None):
        """
        populate a family node with its relatives recursively up to level
        maximum arrests.

        :type network: Network
            The network used as reference to populate the FamilyTree
        :type name: str
            The name of 'target zero' which will be the root of the FamilyTree
        :type maximum_arrests: int
            The maximum amount of arrests and the maximum path length from a
            root to a leaf. Do not populate the tree beyond this number.
        :type parent: None | str
            The name of the parent to be used in adding a FamilyTree node in
            recursive calls.
        :type org: None | int
            The original number of maximum_arrests kept for reference during
            recursive calls.

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> f = FamilyTree()
        >>> f.populate(n1, 'Ethan', 3)
        >>> print(f)
        ('Ethan', 5) , ['Ethan'] , 5
           ('Jacob', 50) , ['Ethan', 'Jacob'] , 55
              ('Liam', 20) , ['Ethan', 'Jacob', 'Liam'] , 75
              ('Emma', 32) , ['Ethan', 'Jacob', 'Emma'] , 87
              ('William', 42) , ['Ethan', 'Jacob', 'William'] , 97
           ('William', 42) , ['Ethan', 'William'] , 47
              ('James', 10) , ['Ethan', 'William', 'James'] , 57
        """
        # in this method, we recursively only add people to the family tree
        # and we don't bother listing nodes that have a path greater than
        # maximum_arrests. To do this, we decrease max_arrests until it hits 0.

        if maximum_arrests == 0:
            # there are no more people to arrest.
            pass
        else:
            if not self.node:
                org = maximum_arrests
                # keep a copy of maximum_arrests for reference later
                # while the  maximum_arrest argument changes for every recursive
                # call.
                self.__add__(network, name)
                parent = name
                relative_nodes = network.list_relative_nodes(name)
                relative_names = [x.data[0] for x in relative_nodes]
                for person in relative_names:
                    if person not in self.seen:
                        # make sure we have not visited this node before
                        self.populate(network, person, maximum_arrests - 1,
                                      parent, org)
            else:
                parent_node = self.family_name_lookup(parent)[0]
                # make sure the seen isn't the length of the original arrests.
                # the following 'if' case is to prevent a scenario where
                # someone is added to a node if the path length is already at
                # its maximum. (same as maximum_arrests)

                if len(parent_node.seen) >= org:
                    self.skip_add(network, name, parent_node.seen, parent)
                else:
                    # add normally
                    self.__add__(network, name, parent)
                parent = name
                relative_nodes = network.list_relative_nodes(name)
                relative_names = [x.data[0] for x in relative_nodes]

                # find the current node
                current_node = self.family_name_lookup(name)
                if len(current_node) == 0:
                    pass
                else:
                    cur = current_node[0]
                    # find the current family tree node and check its 'seen'
                    for person in relative_names:
                        if person not in cur.seen:
                            # make sure you don't revisit the node
                            self.populate(network, person, maximum_arrests - 1,
                                          parent, org)

    def skip_lookup(self, name, seen):
        """
        returns the next node in the family tree that doesn't have the same
        self.seen as the one given. It 'skips' the occurrence of one node and is
        useful in the case where a FamilyTree where self.node (a member)
        occurs more than once.

        :type name: str
            name of the member to be found
        :type seen: list
            this is the seen attribute of the node which is desired to be
            skipped. Avoid a node with this 'seen' attribute.
        """
        if self.node.data[0] == name:
            if self.seen != seen:
                return [self]
        else:
            return [x.skip_lookup(name, seen) for x in self.relatives]

    def skip_add(self, network, name, seen, parent):
        """
        Add someone based on the skipped node as a parent.

        :type network: Network
            A network used as reference.
        :type name: str
            The member's name to be added
        :type seen: list
            This is the seen attribute of the node which is desired to be
            skipped. Avoid a node with this 'seen' attribute.
        :type parent: str
            This is the parent's name.
        """
        node_list = network.name_lookup(name)
        node = node_list[0]
        parent_node_list = self.skip_lookup(parent, seen)

        # The rest of the function is similar to __add__ .
        if len(parent_node_list) == 0:
            pass
        else:
            parent_node = parent_node_list[-1]
            if isinstance(parent_node, list):
                if len(parent_node) != 0:
                    parent_node = parent_node[0]
            # this is the node that has relatives
            fam = FamilyTree(node, [], [], 0)
            # this node is created from one relative to be added
            if isinstance(parent_node, list):
                # this is a case considered for debugging purposes.
                pass
            if not isinstance(parent_node, list):
                parent_node.relatives.append(fam)
                # the new node is a relative of the parent
                fam.seen.extend(parent_node.seen)
                fam.total += parent_node.total
                # the new node inherits both the seen list and total list
                fam.seen.append(node.data[0])
                fam.total += node.data[1]

    def __add__(self, network, name, parent=None):
        """
        Add a new node to the FamilyTree, perhaps based on its parent if the
        FamilyTree is not empty in the beginning.

        :type network: Network
            This is the network topology used as reference
        :rtype: None

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> f = FamilyTree()
        >>> f.__add__(n1, 'Ethan')
        >>> f.node.data
        ('Ethan', 5)
        >>> f.__add__(n1, 'Jacob', 'Ethan')
        >>> print(f)
        ('Ethan', 5) , ['Ethan'] , 5
           ('Jacob', 50) , ['Ethan', 'Jacob'] , 55
        >>> f.__add__(n1, 'William', 'Ethan')
        >>> f.__add__(n1, 'James', 'William')
        >>> print(f)
        ('Ethan', 5) , ['Ethan'] , 5
           ('Jacob', 50) , ['Ethan', 'Jacob'] , 55
           ('William', 42) , ['Ethan', 'William'] , 47
              ('James', 10) , ['Ethan', 'William', 'James'] , 57
        """
        node_list = network.name_lookup(name)
        if len(node_list) == 0:
            pass
        else:
            # find the member node
            node = node_list[0]
            if self.node is None:
                # Case where we have an empty tree and need to add target zero
                self.node = node
                self.seen = []
                # make sure seen is empty before adding anything
                self.seen.append(self.node.data[0])
                # append the member's name
                self.total += self.node.data[1]

            else:
                # must have a parent
                parent_node_list = self.family_name_lookup(parent)
                parent_node = parent_node_list[0]
                # this is the node that has relatives
                fam = FamilyTree(node, [], [], 0)
                # this node is created from one relative to be added
                parent_node.relatives.append(fam)
                # the new node is a relative of the parent
                fam.seen.extend(parent_node.seen)
                fam.total += parent_node.total
                # the new node inherits both the seen list and total list
                fam.seen.append(node.data[0])
                fam.total += node.data[1]
                # add the member's name & asset

    def optimal_arrests(self):
        """
        Return the value with the maximum total of arrests seized from a path
        for target zero.

        :rtype: int

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> f = FamilyTree()
        >>> f.populate(n1, 'Emma', 4)
        >>> f.optimal_arrests()
        144
        >>> p = FamilyTree()
        >>> p.populate(n1, 'Alexander', 4)
        >>> p.optimal_arrests()
        162
        """
        # if self is a leaf, return the seen and total
        if not self.relatives:
            return self.total
        # else, keep looking until you hit a leaf and make sure you get the max
        else:
            return max([x.optimal_arrests() for x in self.relatives])

    def optimal_path(self, arrests):
        """
        Return a path that gives a path of members based on the optimal arrests
        for target zero.

        :type arrests: int
            This is taken directly from self.optimal_arrests().
        :rtype: list of str

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> f = FamilyTree()
        >>> f.populate(n1, 'Emma', 4)
        >>> arrests = f.optimal_arrests()
        >>> arrests
        144
        >>> f.optimal_path(arrests)
        ['Emma', 'Liam', 'Jacob', 'William']
        """
        if self.total == arrests:
            return self.seen
        else:
            return gather_lists([x.optimal_path(arrests) for x in
                                 self.relatives])

    def family_name_lookup(self, name):
        """
        A helper function that returns a list of the single FamilyTree node
        given a member's name.

        :type name: str
            The name of the member who is looked up
        :rtype: List of FamilyTree

        >>> n1 = Network()
        >>> n1.load_log("topology1.txt")
        >>> f = FamilyTree()
        >>> f.__add__(n1, 'Ethan')
        >>> f.node.data
        ('Ethan', 5)
        >>> f.__add__(n1, 'Jacob', 'Ethan')
        >>> print(f)
        ('Ethan', 5) , ['Ethan'] , 5
           ('Jacob', 50) , ['Ethan', 'Jacob'] , 55
        >>> f.__add__(n1, 'William', 'Ethan')
        >>> William = f.family_name_lookup('William')
        >>> William[0].seen
        ['Ethan', 'William']
        """
        if self.node.data[0] == name:
            return [self]
        else:
            return gather_lists(
                    [x.family_name_lookup(name) for x in self.relatives])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # A sample example of how to use a network object
    network = Network()
    network.load_log("topology1.txt")
    member_name = "Sophia"
    print(member_name + "'s sponsor is " + network.sponsor(member_name))
    print(member_name + "'s mentor is " + network.mentor(member_name))
    print(member_name + "'s asset is " + str(network.assets(member_name)))
    print(member_name + "'s childrens are " + str(network.children(member_name)))
    maximum_arrest = 4
    print("The best arrest scenario with the maximum of " + str(maximum_arrest)\
          + " arrests will seize " + str(network.best_arrest_assets(maximum_arrest)))
    print("The best arrest scenario with the maximum of " + str(maximum_arrest)\
          + " arrests is: " + str(network.best_arrest_order(maximum_arrest)))
