import game
import input
import utils


class BehaviourManager:
    """The Bahavoiur manager stores component behevoiurs."""

    def __init__(self, event_manager, entitiy_manager, config=None):
        self.event_manager = event_manager
        self.entity_manager = entitiy_manager
        self.behaviours = {}
        if config is not None:
            self.configure(config)

    def configure(self, config):
        """Configure behaviourse base on a configuration.

        Ars:
            config: {'component_behaviours': [{component_type, name: ''}]}

        """
        if 'component_behaviours' in config:
            for comp_behaviour_config in config['component_behaviours']:
                self.add_comp_behaviour_from_config(comp_behaviour_config)

    def add_comp_behaviour_from_config(self, config):
        """Associates the behaviour specified be the name with the specified
        compoenent_type.

        Args:
            component_type (str): The component type associated with the
                behaviour
            behaviour_impl (str): The implementation of the behaviour.

        """
        impl = config['impl']
        behaviour_class = utils.class_for_name(impl[0], impl[1])
        behaviour = behaviour_class(self.event_manager, self.entity_manager)
        self.add_component_behaviour(config['component_type'], behaviour)

    def add_component_behaviour(self, component_type, behaviour):
        """Register the given behaviour with the specified component type."""
        self.behaviours.update({component_type: behaviour})

    def update(self, round, delta_time):
        """Updates all behaviours for all entitites with a associated
        components."""
        for component_type, behaviour in self.behaviours.iteritems():
            components = self.entity_manager.get_all(component_type)
            for entity, component in components.iteritems():
                behaviour.entity = entity
                behaviour.component = component
                behaviour.update(round, delta_time)


class EntityComponentBehaviour:
    """Implements logic for entities with specific components."""

    def __init__(self, event_manager, entitiy_manager):
        self.entity_manager = entitiy_manager
        self.event_manager = event_manager
        self.entity = None
        self.component = None

    def update(self, round, delta_time):
        pass


class InputBehaviour(EntityComponentBehaviour):
    """Implements User Input. Controls all entites with an InputComponent."""

    def update(self, round, delta_time):
        """Converts input to an appropriate InputAction."""
        # TODO Implement gamestatus aware behaviour manager to keep the turn
        # based logic as central as possible and possibly enable switching
        # between realtime and turn based. (A realtime behaviour would not
        # check for a state
        if game.status == game.G_ROUND_WAITING_INPUT:
            dx = 0
            dy = 0
            if input.is_pressed(
                input.K_LEFT) or input.is_pressed(
                input.K_KP1) or input.is_pressed(
                input.K_KP4) or input.is_pressed(
                    input.K_KP7):
                dx = -1
            if input.is_pressed(
                input.K_RIGHT) or input.is_pressed(
                input.K_KP3) or input.is_pressed(
                input.K_KP6) or input.is_pressed(
                    input.K_KP9):
                dx = dx + 1
            if input.is_pressed(
                input.K_DOWN) or input.is_pressed(
                input.K_KP1) or input.is_pressed(
                input.K_KP2) or input.is_pressed(
                    input.K_KP3):
                dy = 1
            if input.is_pressed(
                input.K_UP) or input.is_pressed(
                input.K_KP7) or input.is_pressed(
                input.K_KP8) or input.is_pressed(
                    input.K_KP9):
                dy = dy - 1

            if dy != 0 or dx != 0:
                self.move(dx, dy)
            elif input.is_pressed(input.K_ENTER):
                # TODO: Implement Targeting Inputs (combined input or
                # sequential?)
                # TODISCUSS: Context actions, autotargeting
                self.use(0, 0)

    def move(self, dx, dy):
        """Throws a MoveAction."""
        # TODO push up the _TURN attribute to EntityComponentBehaviour or
        # BehaviourManager
        self.event_manager.throw(
            'MoveAction_TURN', {
                'entity': self.entity, 'dx': dx, 'dy': dy})

    def use(self, dx, dy):
        """ Throws a UseEntity Event """
        self.event_manager.throw("UseEntityAction_TURN", {
            'user': self.entity, 'direction': (dx, dy)})
