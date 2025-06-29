import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
	const [count, setCount] = useState(0)

	return (
		<>
			<div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-800 to-blue-900 flex flex-col items-center justify-center text-white font-sans p-4">
				<div className="flex space-x-12 mb-10 animate-fade-in">
					<a href="https://vite.dev" target="_blank" rel="noopener noreferrer">
						<img
							src={viteLogo}
							className="w-28 h-28 hover:scale-110 transition-transform duration-300 drop-shadow-lg"
							alt="Vite logo"
						/>
					</a>
					<a href="https://react.dev" target="_blank" rel="noopener noreferrer">
						<img
							src={reactLogo}
							className="w-28 h-28 hover:rotate-12 hover:scale-110 transition-all duration-300 drop-shadow-lg"
							alt="React logo"
						/>
					</a>
				</div>

				<h1 className="text-5xl font-extrabold mb-8 bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 via-pink-500 to-purple-500 animate-pulse">
					Vite + React
				</h1>

				<div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8 w-full max-w-md text-center animate-fade-in-up">
					<button
						onClick={() => setCount((count) => count + 1)}
						className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-purple-600 hover:to-pink-500 text-white font-semibold py-2 px-6 rounded-full shadow-md hover:shadow-lg transition-all duration-300"
					>
						🔥 count is {count}
					</button>
					<p className="mt-6 text-gray-200">
						Edit <code className="bg-black/20 px-2 py-1 rounded">src/App.jsx</code> and save to test HMR
					</p>
				</div>

				<p className="mt-6 text-sm text-gray-300 italic animate-fade-in">
					Click on the logos to explore the tech behind the magic ✨
				</p>
			</div>

		</>
	)
}

export default App
