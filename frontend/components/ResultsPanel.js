import { motion } from 'framer-motion'
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js'
import { Radar } from 'react-chartjs-2'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

const ResultsPanel = ({ results, isLoading, darkMode }) => {
  if (isLoading) {
    return (
      <motion.div
        className="card p-8"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center">
          <motion.div
            className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-100 dark:bg-primary-900 mb-4"
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          >
            <svg className="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
          </motion.div>
          <h3 className="text-lg font-semibold text-secondary-900 dark:text-secondary-100 mb-2">
            Analyzing Code Similarity
          </h3>
          <p className="text-secondary-600 dark:text-secondary-400">
            Processing with multiple AI models...
          </p>
        </div>
      </motion.div>
    )
  }

  if (!results) {
    return (
      <motion.div
        className="card p-8 text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-secondary-500 dark:text-secondary-400">
          <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p className="text-lg font-medium">Ready to Compare Code</p>
          <p className="text-sm">Enter two code snippets and click "Compare" to analyze similarity</p>
        </div>
      </motion.div>
    )
  }

  const getVerdictMessage = (score) => {
    if (score >= 80) return { text: "High Similarity - Potential Plagiarism", color: "text-red-600 dark:text-red-400", bg: "bg-red-100 dark:bg-red-900" }
    if (score >= 60) return { text: "Moderate Similarity - Review Recommended", color: "text-yellow-600 dark:text-yellow-400", bg: "bg-yellow-100 dark:bg-yellow-900" }
    if (score >= 40) return { text: "Low Similarity - Some Common Patterns", color: "text-blue-600 dark:text-blue-400", bg: "bg-blue-100 dark:bg-blue-900" }
    return { text: "Very Low Similarity - Likely Original", color: "text-green-600 dark:text-green-400", bg: "bg-green-100 dark:bg-green-900" }
  }

  const verdict = getVerdictMessage(results.FinalVerdict)

  // Prepare radar chart data
  const radarData = {
    labels: ['Cohere', 'TogetherAI', 'Replicate'],
    datasets: [
      {
        label: 'Similarity Score',
        data: [results.Cohere, results.TogetherAI, results.Replicate],
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: 'rgba(59, 130, 246, 1)',
        pointBackgroundColor: 'rgba(59, 130, 246, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8,
      },
    ],
  }

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      r: {
        angleLines: {
          color: darkMode ? 'rgba(148, 163, 184, 0.3)' : 'rgba(148, 163, 184, 0.5)',
        },
        grid: {
          color: darkMode ? 'rgba(148, 163, 184, 0.3)' : 'rgba(148, 163, 184, 0.5)',
        },
        pointLabels: {
          color: darkMode ? 'rgba(148, 163, 184, 0.8)' : 'rgba(51, 65, 85, 0.8)',
          font: {
            size: 12,
            weight: 'bold',
          },
        },
        ticks: {
          color: darkMode ? 'rgba(148, 163, 184, 0.6)' : 'rgba(51, 65, 85, 0.6)',
          backdrop: {
            color: 'transparent',
          },
        },
        suggestedMin: 0,
        suggestedMax: 100,
      },
    },
  }

  return (
    <motion.div
      className="card p-6"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-6">
        <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-4">
          Similarity Analysis Results
        </h3>
        
        {/* Final Verdict */}
        <motion.div
          className={`rounded-lg p-4 mb-6 ${verdict.bg}`}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className={`font-semibold ${verdict.color}`}>
                Final Verdict: {results.FinalVerdict}%
              </p>
              <p className={`text-sm ${verdict.color}`}>
                {verdict.text}
              </p>
            </div>
            <motion.div
              className={`text-3xl font-bold ${verdict.color}`}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.5, type: "spring", stiffness: 200 }}
            >
              {results.FinalVerdict}%
            </motion.div>
          </div>
        </motion.div>

        {/* Individual Model Scores */}
        <div className="space-y-4 mb-6">
          {Object.entries(results).filter(([key]) => key !== 'FinalVerdict').map(([model, score], index) => (
            <motion.div
              key={model}
              className="space-y-2"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index }}
            >
              <div className="flex justify-between items-center">
                <span className="font-medium text-secondary-700 dark:text-secondary-300">
                  {model}
                </span>
                <span className="font-semibold text-secondary-900 dark:text-secondary-100">
                  {score}%
                </span>
              </div>
              <div className="w-full bg-secondary-200 dark:bg-secondary-700 rounded-full h-3 overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${score}%` }}
                  transition={{ delay: 0.3 + 0.1 * index, duration: 1, ease: "easeOut" }}
                />
              </div>
            </motion.div>
          ))}
        </div>

        {/* Radar Chart */}
        <motion.div
          className="h-64 flex items-center justify-center"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6 }}
        >
          <div className="w-full h-full">
            <Radar data={radarData} options={radarOptions} />
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}

export default ResultsPanel
