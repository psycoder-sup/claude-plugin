#!/bin/bash
# Git Worktree Workspace Manager
# Creates worktrees at ~/.worktree/{project}/{branch} with tmux integration

set -e

# Get project name from git remote or directory
get_project_name() {
    local remote_url
    remote_url=$(git remote get-url origin 2>/dev/null || echo "")
    if [ -n "$remote_url" ]; then
        echo "$remote_url" | sed 's/.*[/:]\([^/]*\)\.git$/\1/' | sed 's/\.git$//'
    else
        basename "$(pwd)"
    fi
}

# Create a new worktree with tmux window
create_worktree() {
    local branch="$1"
    local project
    project=$(get_project_name)
    local worktree_path="$HOME/.worktree/$project/$branch"

    if [ -z "$branch" ]; then
        echo "Error: Branch name required"
        exit 1
    fi

    # Check if worktree already exists
    if git worktree list | grep -q "$worktree_path"; then
        echo "Worktree already exists at: $worktree_path"
        exit 1
    fi

    # Create parent directory
    mkdir -p "$HOME/.worktree/$project"

    # Check if branch exists (local or remote)
    if git show-ref --verify --quiet "refs/heads/$branch" 2>/dev/null; then
        echo "Creating worktree for existing local branch: $branch"
        git worktree add "$worktree_path" "$branch"
    elif git show-ref --verify --quiet "refs/remotes/origin/$branch" 2>/dev/null; then
        echo "Creating worktree for remote branch: origin/$branch"
        git worktree add "$worktree_path" "$branch"
    else
        echo "Creating worktree with new branch: $branch"
        git worktree add -b "$branch" "$worktree_path"
    fi

    # Create tmux window with dev layout if in tmux session
    if [ -n "$TMUX" ]; then
        # Create new window
        tmux new-window -n "$branch" -c "$worktree_path"

        # Split horizontally (top/bottom) - creates new pane at bottom with focus
        tmux split-window -v -c "$worktree_path"

        # Wait for shells to initialize
        sleep 0.3

        # Run claude in bottom pane (current pane after split)
        tmux send-keys "claude" Enter

        # Focus on top pane (use -U for relative selection, works with any pane-base-index)
        tmux select-pane -U

        echo "Created tmux window '$branch' with dev layout (top: terminal, bottom: claude)"
    else
        echo "Not in tmux session. To open worktree:"
        echo "  cd $worktree_path"
    fi

    echo "Worktree created at: $worktree_path"
}

# List all worktrees
list_worktrees() {
    echo "=== Git Worktrees ==="
    git worktree list
    echo ""

    if [ -n "$TMUX" ]; then
        echo "=== Tmux Windows ==="
        tmux list-windows -F "  #{window_index}: #{window_name}#{?window_active, (active),}"
    fi
}

# Remove a worktree and its tmux window
remove_worktree() {
    local name="$1"
    local project
    project=$(get_project_name)
    local worktree_path="$HOME/.worktree/$project/$name"

    if [ -z "$name" ]; then
        echo "Error: Worktree name required"
        echo "Available worktrees:"
        git worktree list
        exit 1
    fi

    # Check if worktree exists
    if ! git worktree list | grep -q "$worktree_path"; then
        echo "Worktree not found at: $worktree_path"
        echo "Available worktrees:"
        git worktree list
        exit 1
    fi

    # Remove worktree
    echo "Removing worktree: $worktree_path"
    git worktree remove "$worktree_path" --force

    # Kill tmux window if exists
    if [ -n "$TMUX" ]; then
        if tmux list-windows -F "#{window_name}" | grep -q "^${name}$"; then
            tmux kill-window -t "$name"
            echo "Killed tmux window: $name"
        fi
    fi

    # Clean up empty project directory
    rmdir "$HOME/.worktree/$project" 2>/dev/null || true

    echo "Worktree removed successfully"
}

# Main
case "${1:-}" in
    create)
        create_worktree "$2"
        ;;
    list)
        list_worktrees
        ;;
    remove|delete)
        remove_worktree "$2"
        ;;
    *)
        echo "Usage: worktree.sh <command> [args]"
        echo ""
        echo "Commands:"
        echo "  create <branch>  Create worktree for branch with tmux window"
        echo "  list             List existing worktrees and tmux windows"
        echo "  remove <name>    Remove worktree and kill tmux window"
        exit 1
        ;;
esac
