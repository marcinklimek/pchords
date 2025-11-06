/**
 * Settings panel component for PChords.
 */

import { PracticeSettings } from '../../hooks/useSettings'

interface SettingsProps {
  settings: PracticeSettings
  onUpdate: (updates: Partial<PracticeSettings>) => void
  onClose: () => void
}

export function Settings({ settings, onUpdate, onClose }: SettingsProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-xl shadow-2xl p-6 max-w-md w-full mx-4">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-white">Settings</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors text-2xl"
          >
            ×
          </button>
        </div>

        {/* Settings Options */}
        <div className="space-y-4">
          {/* Root Note Practice */}
          <div className="bg-gray-700 rounded-lg p-4">
            <label className="flex items-center justify-between cursor-pointer">
              <div>
                <div className="text-white font-semibold">Root Note Practice</div>
                <div className="text-gray-400 text-sm mt-1">
                  Play root note (bass) with left hand + chord with right hand
                </div>
              </div>
              <div className="ml-4">
                <input
                  type="checkbox"
                  checked={settings.rootNotePractice}
                  onChange={(e) => onUpdate({ rootNotePractice: e.target.checked })}
                  className="w-6 h-6 text-primary-600 bg-gray-700 border-gray-600 rounded focus:ring-primary-500 focus:ring-2"
                />
              </div>
            </label>
          </div>

          {/* Info Box */}
          {settings.rootNotePractice && (
            <div className="bg-blue-900 bg-opacity-30 border border-blue-700 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <span className="text-blue-400 text-xl">ℹ️</span>
                <div className="text-blue-200 text-sm">
                  <strong>Root Note Practice Mode:</strong>
                  <ul className="mt-2 space-y-1 list-disc list-inside">
                    <li>Orange square (■) = Root note for left hand</li>
                    <li>Blue circles (○) = Chord notes for right hand</li>
                    <li>You must play both to advance to next chord</li>
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Close Button */}
        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  )
}
