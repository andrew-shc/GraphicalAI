from src.debugger import *


class World:
    """
    Manages all components and system (and entities)

    ATTRIBUTES
    ----------

    Tag -> Compact Entity ID with the value at the same index as at the Entities
    Entities -> Refers to component for data and requirements
    Component -> All the registered components
    Container -> All the data organized by components
    System -> All the registered system (or registered functions)

    # TODO: [IF] Implement compact container and non-compact container if needed
    COMPACT STORAGE -> HAS NO KEY, PURE DATA; ORDERED; MORE CPU
    NON-COMPACT STORAGE -> HAS KEYS; ORDERLESS; MORE DATA

    Compact storage is the default

    EID ~ List of Entity ID
    ENTITIES ~ List of Entities Data
    """

    UNIQ_ID = 0  # compact ID

    TAG = []  # [EID, EID, EID, ...]
    ENTITIES = []  # [ENTITY, ENTITY, ENTITY, ...]
    COMPONENT = []  # components registered; for key and index for container
    CONTAINER = []  # [[data, data, ...], [data, ...], ...]; to store data; 2d data array
    SYSTEM = []  # registered systems (i.e. functions)
    GLOBAL = {}  # global variable

    DESTROYING = []  # entities to be destroyed

    def __init__(self, component, system):
        """
        :param component: Components to be registered with the respective World()
        :param system: Systems to be registered for execution in the respective World()
        """

        for c in component:
            if component.count(c) > 1:
                error(f"Duplicate component <{c}> when initializing")

        self.COMPONENT = component
        self.SYSTEM = system
        for _ in component:  # initilize the data space in the container (data 2D array)
            self.CONTAINER.append([])

    # ==== fundamental method ====

    def create(self, **kwargs):
        """ creates anew entity from list of registered components
        :param **kwargs: Selected component (key) assigning a value (val) to the respective component
        """

        for k in kwargs:
            if k not in self.COMPONENT:
                error(f"Entity creation passed in unregistered component <{k}>")

        ID = []  # [0, 3, 4, 5, 2, -1]; -1 means no value for each registered components
        dead = True  # if all the index in the entity is -1 (null pointer)
        for ind, cmpn in enumerate(self.COMPONENT):
            if cmpn in kwargs:
                self.CONTAINER[ind].append(kwargs[cmpn])  # appends the data to the container
                ID.append(len(self.CONTAINER[ind])-1)  # appends the index of that data
                dead = False
            else:
                ID.append(-1)
        if dead:
            self.DESTROYING.append(ID)
        self.ENTITIES.append(ID)  # the index
        self.TAG.append(self.allocate_id(self.TAG))  # append compact index

        info("Entity Created:", self.allocate_id(self.TAG))

    def destroy(self, eid):
        """ destroy the entity through ID
        :param eid: Destroys entity by ID
        """
        self.ENTITIES.remove(eid)
        self.DESTROYING.append(eid)

        info("Entity Destroyed", eid)

    def flush(self):
        """ cleans all the dead data in the container """

        info("Dead Entity Flushed")

    def execute(self, prop, ):
        """ executes all the function; the function manages the entities
        :param prop: dictionary to be updated on self.GLOBAL global dictionary
        """

        self.GLOBAL = prop
        for s in self.SYSTEM:
            s(self, self.GLOBAL)

    @staticmethod
    def allocate_id(lst):
        """ to allocate an id that is open for anew entity
        :return: index allocated to be open
        """

        for ind, i in enumerate(sorted(lst)):
            if ind != i: return ind
        return len(lst)

    def short_id(self, eid):
        """ To find the short id of the entity id
        :param eid: Entity ID's
        :return: Short ID (uint tag)
        """
        return self.TAG[self.ENTITIES.index(eid)]

    # ==== feature methods ====

    def organize(self):
        """ organize the container by components (hierachy) """
        pass

    def entity(self, eid, cmpn):
        """ get entity by list of required components
        :param eid: List of entity ID to be used on
        :param cmpn: List of requested component
        :return: Returns list of matched entity
        """

        for r in cmpn:
            if r not in self.COMPONENT:
                error(f"System <{caller_name()}> used unregistered component {r}")

        # translates requested string components to translated required id
        ID_KEY = [d for d in map(lambda c: 0 if c not in cmpn else 1, self.COMPONENT)]
        MATCHED = []  # entity passed the requirement
        for entity in eid:
            REQUESTED = True
            for id, c in zip(ID_KEY, entity):
                if id == 1 and c == -1:
                    REQUESTED = False
                    break
            if REQUESTED:
                MATCHED.append(entity)  # appends entity ID
        return MATCHED

    def entity_data(self, eid, req=None):
        """ translates list of entity id into actual usable data
        :param eid: list of Entity ID to be processed into usable data for systems
        :param req: entities that has the components listed in req; mainly to save performance
        :param _strict =False:
        :return: Returns processed Entities
        """

        combined = []
        if req is not None:
            for idf in eid:  # each entity in entity list
                passed = True
                data = {}
                for ind, c in enumerate(idf):  # each component ID in full entity ID
                    if c == -1 and self.COMPONENT[ind] in req:
                        passed = False
                        break
                    elif c != -1:
                        data[self.COMPONENT[ind]] = self.CONTAINER[ind][c]
                if passed: combined.append(data)
        else:
            for idf in eid:  # each entity in entity list
                data = {}
                for ind, c in enumerate(idf):  # each component ID in full entity ID
                    if c != -1: data[self.COMPONENT[ind]] = self.CONTAINER[ind][c]
                combined.append(data)
        return combined

    def entity_pp_cmpnt(self, ent, lst, strict=False):
        """ Entity Post-Processing: Process by components

        :param ent: list of entity data to post-process on
        :param lst: list of required components to modify the entity data
        :param strict: False, returns matched entities
                        True, returns matched entities with only the requested components
        :return: post processed entity data
        """

        RESULT = []
        if not strict:
            for e in ent:
                REQ = True
                for c in lst:
                    if c not in list(e):
                        REQ = False
                if REQ: RESULT.append(e)
        else:
            for e in ent:
                DATA = {}
                REQ = True
                for c in lst:
                    if c not in list(e):
                        REQ = False
                    else:
                        DATA[c] = e[c]
                if REQ: RESULT.append(DATA)
        return RESULT

    def entity_pp_strip(self, ent, strict, **kwargs):
        """ Entity Post-Processing: Process by component's value

        :param ent: list of entity data to post-process on
        :param strict: False, returns matched entities
                        True, returns matched entities with only the requested components
                        *NOTE: (just returns same as kwargs; only useful for counting and related)
        :param kwargs: key as the component name required and value to process entity that have the same value
        :return:
        """
        RESULT = []
        if not strict:
            for e in ent:
                REQ = True
                for c in kwargs:
                    if c in list(e):
                        if kwargs[c] != e[c]:
                            REQ = False
                    else:
                        REQ = False
                if REQ: RESULT.append(e)
        else:
            for e in ent:
                DATA = {}
                REQ = True
                for c in kwargs:
                    if c in list(e):
                        if kwargs[c] != e[c]:
                            REQ = False
                        else:
                            DATA[c] = e[c]
                    else:
                        REQ = False
                if REQ: RESULT.append(DATA)
        return RESULT

    def entity_pp_extc(self, ent, cmpnt):
        """ Entity Post-Processing: Extract single component from a list of entities

        :param cmpnt: single component to extract
        :return: list of component from entities
        """
        extrctd = []

        if cmpnt not in self.COMPONENT:
            raise ValueError(f"Component {cmpnt} is not registered in the World instance {self}")

        for e in ent:
            if cmpnt not in list(e):
                raise ValueError(f"Entity {e} does not contain component {cmpnt}")
            else:
                extrctd.append(e[cmpnt])
        return extrctd

    def entity_save(self, eid, ent_dt):
        """ to save the data from entity dictionary into the container
        :param eid: Entity ID to find the reference to the container
        :param ent_dt: Data the Systems edited to be saved into the container
        """

        for ind, c in enumerate(eid):
            if self.COMPONENT[ind] in ent_dt:  # components received from the eid is in the ent_data
                if c != -1:  # has pointer for that component to refer data, implying there is data
                    self.CONTAINER[ind][c] = ent_dt[self.COMPONENT[ind]]
                else:  # nullptr component whilst still in-bound to ent_dt
                    error(f"Entity ID, <{eid}>, does not align with the data (in order), <{list(ent_dt.keys())}>")
            else:
                if c == 1:  # has the pointer but not in ent_dt, definite no-no
                    error(f"Entity ID, <{eid}>, does not align with the data (in order), <{list(ent_dt.keys())}>")
