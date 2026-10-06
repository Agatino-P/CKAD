# Nano gotchas

- On macOS, `/usr/bin/nano` is a symbolic link to UW Pico 5.09, not GNU nano.\
  Pico has no mark-based copy and no undo, so practice with GNU nano from `brew install nano`.
- On macOS every `Alt` shortcut needs the Option key mapped as Meta.\
  On the Keychron K10 in Mac mode, the key labelled `Alt` sends Option and the key labelled `Windows` sends Cmd.\
  iTerm2: Settings, Profiles, Keys, General, "Left Option key" set to `Esc+`, and "Right Option key" too for the right-hand `Alt`.\
  VS Code terminal: set `"terminal.integrated.macOptionIsMeta": true` in `settings.json`.\
  Terminal.app: Settings, Profiles, Keyboard, "Use Option as Meta key".\
  Without that mapping, press `Esc` then the key: `Esc` then `6` equals `Alt+6`.
- The CKAD exam runs on a Linux remote desktop, where `Alt` works with no setup.
