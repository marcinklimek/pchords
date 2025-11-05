/**
 * Application header component.
 */

interface HeaderProps {
  onSettingsClick?: () => void
}

export function Header({ onSettingsClick }: HeaderProps) {
  return (
    <header className="bg-gray-900 border-b border-gray-800">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-3xl font-bold text-white">
              🎹 <span className="text-primary-500">PChords</span>
            </h1>
            <span className="text-sm text-gray-400 font-mono">v2.0</span>
          </div>

          <nav className="flex items-center gap-4">
            <button
              onClick={onSettingsClick}
              className="px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
            >
              ⚙️ Settings
            </button>

            <a
              href="https://github.com/marcinklimek/pchords"
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
            >
              📚 GitHub
            </a>
          </nav>
        </div>
      </div>
    </header>
  )
}
