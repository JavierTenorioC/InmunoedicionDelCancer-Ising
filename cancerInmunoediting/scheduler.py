from typing import Type, Callable
import mesa

class RandomActivationByTypeFiltered(mesa.time.RandomActivationByType):
    """
    Un scheduler que anula el metodo get_type_count para permitir el filtrado
    de agentes mediante una funcion antes de contarlos.

    Ejemplo:
    >>> scheduler = RandomActivationByTypeFiltered(modelo)
    >>> scheduler.get_type_count(AgenteA, lambda agente: agente.algun_atributo > 10)
    """

    def get_type_count(
        self,
        type_class: Type[mesa.Agent],
        filter_func: Callable[[mesa.Agent], bool] = None,
    ) -> int:
        """
        Devuelve el numero actual de agentes de un tipo especifico en la cola que satisfacen la funcion de filtro.
        """
        count = 0
        for agent in self.agents_by_type[type_class].values():
            if filter_func is None or filter_func(agent):
                count += 1
        return count
    
    def get_count(
        self,
        filter_func: Callable[[mesa.Agent], bool] = None,
    ) -> int:
        """
        Devuelve el numero actual de agentes en la cola que satisfacen la funcion de filtro.
        """
        count = 0
        for agent in self.agent_buffer(shuffled=False):
            if filter_func is None or filter_func(agent):
                count += 1
        return count