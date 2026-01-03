# psycoder-tools

A collection of Claude Code plugins for enhanced development workflows.

## Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| [base](./base) | 1.0.1 | Git workflow commands with conventional commits and emoji support |
| [task](./task) | 1.1.0 | Task planning and execution system with code analysis agents |
| [nearville-figma](./nearville-figma) | 1.0.1 | Figma design-to-code implementation for React Native |

## Installation

Add this marketplace to your Claude Code configuration:

```json
{
  "plugins": {
    "marketplaces": [
      {
        "name": "psycoder-tools",
        "source": "path/to/claude-plugin"
      }
    ]
  }
}
```

## Available Commands

### Git Workflows (base)
- `/commit` - Create well-formatted commits with conventional format and emoji
- `/create-pr` - Create pull requests with structured descriptions

### Task Management (task)
- `/plan-task` - Plan features with codebase analysis and task file generation
- `/execute-task` - Execute planned tasks in batches with review checkpoints

### Figma Integration (nearville-figma)
- `/implement-design` - Translate Figma designs to React Native code
- `/code-connect` - Connect Figma components to code implementations
- `/design-system-rules` - Generate design system rules for your project

## Author

**Psycoder SUP** - parksang1993@gmail.com

## License

MIT
