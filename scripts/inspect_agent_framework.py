from __future__ import annotations

import inspect
import pkgutil

import agent_framework
import agent_framework.azure as azure_agent_framework


def main() -> None:
    print("agent_framework package:")
    print(agent_framework)
    print()

    print("agent_framework.azure exports:")
    azure_names = dir(azure_agent_framework)
    for name in azure_names:
        if "Agent" in name or "Client" in name or "Foundry" in name or "Chat" in name:
            print("-", name)

    print()
    print("agent_framework.azure modules:")
    if hasattr(azure_agent_framework, "__path__"):
        for module in pkgutil.iter_modules(azure_agent_framework.__path__):
            print("-", module.name)

    print()
    if hasattr(azure_agent_framework, "DurableAIAgentClient"):
        cls = getattr(azure_agent_framework, "DurableAIAgentClient")
        print("DurableAIAgentClient signature:")
        try:
            print(inspect.signature(cls))
        except Exception as exc:
            print(f"Could not inspect class signature: {exc}")

        print()
        print("DurableAIAgentClient methods:")
        for name, value in inspect.getmembers(cls):
            if not name.startswith("_") and callable(value):
                print("-", name)


if __name__ == "__main__":
    main()
