from dataclasses import dataclass, fields, asdict
from typing import Type, Dict, Any


@dataclass
class Serializable:
    def customer_serialize(self) -> Dict[str, Any]:
        serialized_data = asdict(self)
        for field in fields(self):
            value = getattr(self, field.name)
            if hasattr(value, 'customer_serialize'):
                serialized_data[field.name] = value.customer_serialize()
            elif isinstance(value, list) and value and hasattr(value[0], 'customer_serialize'):
                serialized_data[field.name] = [item.customer_serialize() for item in value]
        return serialized_data

    @classmethod
    def init_from_dict(cls: Type['Serializable'], data: Dict[str, Any]) -> 'Serializable':
        init_args = {}
        for field in fields(cls):
            field_value = data.get(field.name)
            if hasattr(field.type, 'init_from_dict') and isinstance(field_value, dict):
                init_args[field.name] = field.type.init_from_dict(field_value)
            elif (isinstance(field_value, list) and
                  field.type.__args__ and
                  hasattr(field.type.__args__[0], 'init_from_dict') and
                  all(isinstance(i, dict) for i in field_value)):
                init_args[field.name] = [field.type.__args__[0].init_from_dict(item) for item in field_value]
            else:
                init_args[field.name] = field_value
        return cls(**init_args)


@dataclass
class Demo(Serializable):
    name: str
    age: int


if __name__ == '__main__':
    demo = Demo(name='Tom', age=18)
    demo.customer_serialize()
