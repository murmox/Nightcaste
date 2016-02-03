"""The model represents backing storage for entities."""


class EntityManager:
    """The EntityManager is the interface for all systems to create and retrieve
    entites e.g their components"""

    def __init__(self):
        self.last_id = -1l
        self.component_manager = ComponentManager()
        self.blueprint_manager = BlueprintManager()

    def create_entity(self):
        self.last_id += 1l
        return self.last_id

    def create_entity_from_configuration(self, configuration):
        entity = self.create_entity()
        self.component_manager.add_components(entity, configuration)
        return entity

    def create_entity_from_blueprint(self, blueprint):
        configuration = self.blueprint_manager.create_configuration(blueprint)
        return self.create_entity_from_configuration(configuration)


class ComponentManager:
    """ The Component manager stores the components for all entities (represented by
    int entity_id) """

    def __init__(self):
        # Two-dimensional dictionary holding the components of all entities
        # {component_type: {entity_id: Component}}
        self.components = {}

    def add_component(self, entity_id, component):
        component_type = component.type()
        component_dict = self.components.get(component_type, {})
        if (component_dict is not None):
            component_dict = {}
            self.components[component_type] = component_dict
        self.components[component_type][entity_id] = component

    def add_components(self, entity_id, configuration):
        pass

    def remove_component(self, entity_id, component_type):
        pass

    def get_component(self, entity_id, component_type):
        pass

    def get_all_of_type(self, component_type):
        pass


class BlueprintManager:
    """Points the a blueprint file which contains information about the
    structure of an entity"""

    def create_configuration(self, blueprint):
        """TODO: either load prefetched configuration or lazy load it here.
        Since loading a bluebrint involves IO it may be advisable to prefetch
        the configuration into a dictionary are at least cache on first
        access"""
        return EntityConfiguration()


class EntityConfiguration:
    """Stores the necessary information the construct an entity

        TODO:
            - Select better data structure than nested dictionaries
              => may be a combined key 'Position.x': value
              => Complete object structure: Component with a List of Attributes
                 an Attribute is a key value pair
            - Provide easy acceess to all information

    """

    def __init__(self):
        self.components = {}

    def add_attribute(self, component, name, value):
        """Add an attribute for the specified component

            TODO: May select better structure than dictionaries"""
        if component not in self.components:
            self.components.update({component: {name: value}})
        else:
            component_attributes = self.components[component]
            component_attributes.update({name: value})

    def get_attributes(self, component):
        if component not in self.components:
            return {}

        return self.components[component]