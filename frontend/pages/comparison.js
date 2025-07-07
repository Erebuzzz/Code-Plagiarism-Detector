import { useState } from 'react'
import Head from 'next/head'
import { motion } from 'framer-motion'
import CodeEditor from '../components/CodeEditor'
import ThemeToggle from '../components/ThemeToggle'
import Link from 'next/link'

export default function Comparison({ darkMode, toggleDarkMode }) {
  const [code1, setCode1] = useState('')
  const [code2, setCode2] = useState('')
  const [detailedResults, setDetailedResults] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleDetailedCompare = async () => {
    if (!code1.trim() || !code2.trim()) {
      setError('Please enter code in both editors')
      return
    }

    setIsLoading(true)
    setError(null)
    setDetailedResults(null)

    try {
      const response = await fetch('/detailed-check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code1: code1.trim(),
          code2: code2.trim(),
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      if (data.error) {
        throw new Error(data.error)
      }

      setDetailedResults(data)
    } catch (err) {
      console.error('Detailed comparison error:', err)
      setError(err.message || 'Failed to perform detailed comparison. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleClearAll = () => {
    setCode1('')
    setCode2('')
    setDetailedResults(null)
    setError(null)
  }

  const loadExample = () => {
    const example1 = `def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Test the function
numbers = [3, 6, 8, 10, 1, 2, 1]
print("Original:", numbers)
print("Sorted:", quicksort(numbers))`

    const example2 = `def quick_sort(array):
    if len(array) <= 1:
        return array
    pivot_element = array[len(array) // 2]
    smaller = [item for item in array if item < pivot_element]
    equal = [item for item in array if item == pivot_element]
    larger = [item for item in array if item > pivot_element]
    return quick_sort(smaller) + equal + quick_sort(larger)

# Testing the sorting algorithm
test_array = [3, 6, 8, 10, 1, 2, 1]
print("Before sorting:", test_array)
print("After sorting:", quick_sort(test_array))`

    setCode1(example1)
    setCode2(example2)
    setDetailedResults(null)
    setError(null)
  }

  const getSimilarityColor = (score) => {
    if (score >= 80) return 'text-red-600 dark:text-red-400'
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400'
    if (score >= 40) return 'text-blue-600 dark:text-blue-400'
    return 'text-green-600 dark:text-green-400'
  }

  const getSimilarityBadge = (score) => {
    if (score >= 80) return 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
    if (score >= 60) return 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200'
    if (score >= 40) return 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200'
    return 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
  }

  const getComplexityLevel = (score) => {
    if (score <= 5) return { level: 'Low', color: 'text-green-600 dark:text-green-400' }
    if (score <= 10) return { level: 'Moderate', color: 'text-yellow-600 dark:text-yellow-400' }
    if (score <= 15) return { level: 'High', color: 'text-orange-600 dark:text-orange-400' }
    return { level: 'Very High', color: 'text-red-600 dark:text-red-400' }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 to-primary-50 dark:from-secondary-900 dark:to-secondary-800 transition-all duration-300">
      <Head>
        <title>Detailed Comparison - AI Code Plagiarism Detector</title>
        <meta name="description" content="Detailed side-by-side code comparison with comprehensive analysis" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="container mx-auto px-4 py-8">
        {/* Header with Navigation */}
        <motion.header
          className="text-center mb-12"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex justify-between items-center mb-8">
            <motion.div
              className="flex items-center space-x-4"
              whileHover={{ scale: 1.02 }}
            >
              <Link href="/" className="btn-secondary flex items-center space-x-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                <span>Back to Home</span>
              </Link>
            </motion.div>
            
            <motion.div
              className="flex items-center space-x-2"
              whileHover={{ scale: 1.05 }}
            >
              <svg className="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2v0M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
              </svg>
              <h1 className="text-4xl font-bold gradient-text">
                Detailed Comparison
              </h1>
            </motion.div>
            
            <div className="flex items-center space-x-4">
              <Link href="/analysis" className="btn-secondary">
                Code Analysis
              </Link>
              <ThemeToggle darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
            </div>
          </div>
          
          <motion.p
            className="text-xl text-secondary-600 dark:text-secondary-400 mb-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            Comprehensive side-by-side code analysis with detailed metrics
          </motion.p>

          <motion.div
            className="flex flex-wrap justify-center gap-4 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <motion.button
              onClick={loadExample}
              className="btn-secondary"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Load Example
            </motion.button>
            <motion.button
              onClick={handleClearAll}
              className="btn-secondary"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Clear All
            </motion.button>
          </motion.div>
        </motion.header>

        {/* Error Message */}
        {error && (
          <motion.div
            className="mb-6 p-4 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 rounded-lg"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {error}
            </div>
          </motion.div>
        )}

        {/* Code Editors */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <CodeEditor
              value={code1}
              onChange={setCode1}
              label="Code Snippet 1"
              placeholder="Paste your first code snippet here..."
              darkMode={darkMode}
            />
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <CodeEditor
              value={code2}
              onChange={setCode2}
              label="Code Snippet 2"
              placeholder="Paste your second code snippet here..."
              darkMode={darkMode}
            />
          </motion.div>
        </div>

        {/* Compare Button */}
        <motion.div
          className="flex justify-center mb-8"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <button
            onClick={handleDetailedCompare}
            disabled={isLoading || !code1.trim() || !code2.trim()}
            className={`btn-primary px-8 py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center space-x-2 ${
              isLoading ? 'cursor-wait' : ''
            }`}
          >
            {isLoading ? (
              <>
                <motion.svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </motion.svg>
                <span>Performing Detailed Analysis...</span>
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2v0M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
                </svg>
                <span>Detailed Compare</span>
              </>
            )}
          </button>
        </motion.div>

        {/* Detailed Results */}
        {detailedResults && (
          <motion.div
            className="space-y-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            {/* Overall Similarity */}
            <div className="card p-6">
              <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-4">
                Overall Similarity
              </h3>
              <div className="flex items-center justify-between mb-4">
                <span className="text-lg font-semibold">Combined Score:</span>
                <span className={`text-2xl font-bold ${getSimilarityColor(detailedResults.similarity?.combined_score || 0)}`}>
                  {(detailedResults.similarity?.combined_score || 0).toFixed(1)}%
                </span>
              </div>
              <div className="grid md:grid-cols-3 gap-4">
                {Object.entries(detailedResults.similarity?.individual_scores || {}).map(([model, score]) => (
                  <div key={model} className="text-center">
                    <div className="text-sm text-secondary-600 dark:text-secondary-400 mb-1">
                      {model.charAt(0).toUpperCase() + model.slice(1)}
                    </div>
                    <div className={`text-lg font-semibold ${getSimilarityColor(score)}`}>
                      {score.toFixed(1)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Side-by-side Analysis */}
            <div className="grid lg:grid-cols-2 gap-8">
              {/* Code 1 Analysis */}
              <div className="card p-6">
                <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-4">
                  Code 1 Analysis
                </h3>
                <div className="space-y-4">
                  {/* Structure */}
                  <div>
                    <h4 className="font-semibold text-secondary-800 dark:text-secondary-200 mb-2">Structure</h4>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-secondary-600 dark:text-secondary-400">Lines:</span>
                        <span className="ml-2 font-medium">{detailedResults.code1_analysis?.structure?.lines || 0}</span>
                      </div>
                      <div>
                        <span className="text-secondary-600 dark:text-secondary-400">Functions:</span>
                        <span className="ml-2 font-medium">{detailedResults.code1_analysis?.structure?.functions || 0}</span>
                      </div>
                      <div>
                        <span className="text-secondary-600 dark:text-secondary-400">Classes:</span>
                        <span className="ml-2 font-medium">{detailedResults.code1_analysis?.structure?.classes || 0}</span>
                      </div>
                      <div>
                        <span className="text-secondary-600 dark:text-secondary-400">Comments:</span>
                        <span className="ml-2 font-medium">{detailedResults.code1_analysis?.structure?.comments || 0}</span>
                      </div>
                    </div>
                  </div>

                  {/* Complexity */}
                  <div>
                    <h4 className="font-semibold text-secondary-800 dark:text-secondary-200 mb-2">Complexity</h4>
                    <div className="flex items-center justify-between">
                      <span className="text-secondary-600 dark:text-secondary-400">Cyclomatic:</span>
                      <div className="flex items-center space-x-2">
                        <span className="font-medium">{detailedResults.code1_analysis?.complexity?.cyclomatic || 0}</span>
                        <span className={`px-2 py-1 rounded text-xs ${getComplexityLevel(detailedResults.code1_analysis?.complexity?.cyclomatic || 0).color}`}>
                          {getComplexityLevel(detailedResults.code1_analysis?.complexity?.cyclomatic || 0).level}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* AI Detection */}
                  <div>
                    <h4 className="font-semibold text-secondary-800 dark:text-secondary-200 mb-2">AI Detection</h4>
                    <div className="flex items-center justify-between">
                      <span className="text-secondary-600 dark:text-secondary-400">AI Generated:</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        detailedResults.code1_analysis?.ai_detection?.is_ai_generated
                          ? 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                          : 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                      }`}>
                        {detailedResults.code1_analysis?.ai_detection?.is_ai_generated ? 'Likely' : 'Unlikely'}
                      </span>
                    </div>
                    <div className="mt-2 text-sm text-secondary-600 dark:text-secondary-400">
                      Confidence: {(detailedResults.code1_analysis?.ai_detection?.confidence || 0).toFixed(1)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Code 2 Analysis */}
              <div className="card p-6">
                <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-4">
                  Code 2 Analysis
                </h3>
                <div className="space-y-4">
                  {/* Structure */}
                  <div>
                    <h4 className="font-semibold text-secondary-800 dark:text-secondary-200 mb-2">Structure</h4>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-secondary-600 dark:text-secondary-400">Lines:</span>
                        <span className="ml-2 font-medium">{detailedResults.code2_analysis?.structure?.lines || 0}</span>
                      </div>
                      <div>
                        <span className="text-secondary-600 dark:text-secondary-400">Functions:</span>
                        <span className="ml-2 font-medium">{detailedResults.code2_analysis?.structure?.functions || 0}</span>
                      </div>
                      <div>
                        <span className="text-secondary-600 dark:text-secondary-400">Classes:</span>
                        <span className="ml-2 font-medium">{detailedResults.code2_analysis?.structure?.classes || 0}</span>
                      </div>
                      <div>
                        <span className="text-secondary-600 dark:text-secondary-400">Comments:</span>
                        <span className="ml-2 font-medium">{detailedResults.code2_analysis?.structure?.comments || 0}</span>
                      </div>
                    </div>
                  </div>

                  {/* Complexity */}
                  <div>
                    <h4 className="font-semibold text-secondary-800 dark:text-secondary-200 mb-2">Complexity</h4>
                    <div className="flex items-center justify-between">
                      <span className="text-secondary-600 dark:text-secondary-400">Cyclomatic:</span>
                      <div className="flex items-center space-x-2">
                        <span className="font-medium">{detailedResults.code2_analysis?.complexity?.cyclomatic || 0}</span>
                        <span className={`px-2 py-1 rounded text-xs ${getComplexityLevel(detailedResults.code2_analysis?.complexity?.cyclomatic || 0).color}`}>
                          {getComplexityLevel(detailedResults.code2_analysis?.complexity?.cyclomatic || 0).level}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* AI Detection */}
                  <div>
                    <h4 className="font-semibold text-secondary-800 dark:text-secondary-200 mb-2">AI Detection</h4>
                    <div className="flex items-center justify-between">
                      <span className="text-secondary-600 dark:text-secondary-400">AI Generated:</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        detailedResults.code2_analysis?.ai_detection?.is_ai_generated
                          ? 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                          : 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                      }`}>
                        {detailedResults.code2_analysis?.ai_detection?.is_ai_generated ? 'Likely' : 'Unlikely'}
                      </span>
                    </div>
                    <div className="mt-2 text-sm text-secondary-600 dark:text-secondary-400">
                      Confidence: {(detailedResults.code2_analysis?.ai_detection?.confidence || 0).toFixed(1)}%
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Comparison Insights */}
            {detailedResults.comparison_insights && (
              <div className="card p-6">
                <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-4">
                  Comparison Insights
                </h3>
                <div className="space-y-4">
                  {detailedResults.comparison_insights.structural_similarity && (
                    <div>
                      <h4 className="font-semibold text-secondary-800 dark:text-secondary-200 mb-2">
                        Structural Similarity
                      </h4>
                      <p className="text-secondary-600 dark:text-secondary-400">
                        {detailedResults.comparison_insights.structural_similarity}
                      </p>
                    </div>
                  )}
                  {detailedResults.comparison_insights.style_similarity && (
                    <div>
                      <h4 className="font-semibold text-secondary-800 dark:text-secondary-200 mb-2">
                        Style Similarity
                      </h4>
                      <p className="text-secondary-600 dark:text-secondary-400">
                        {detailedResults.comparison_insights.style_similarity}
                      </p>
                    </div>
                  )}
                  {detailedResults.comparison_insights.potential_plagiarism_indicators && 
                   detailedResults.comparison_insights.potential_plagiarism_indicators.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-secondary-800 dark:text-secondary-200 mb-2">
                        Potential Plagiarism Indicators
                      </h4>
                      <ul className="list-disc list-inside space-y-1 text-secondary-600 dark:text-secondary-400">
                        {detailedResults.comparison_insights.potential_plagiarism_indicators.map((indicator, index) => (
                          <li key={index}>{indicator}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </motion.div>
        )}

        {/* Footer */}
        <motion.footer
          className="mt-16 text-center text-secondary-500 dark:text-secondary-400"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <p className="text-sm">
            Built with ❤️ for the developer community • 
            <a href="https://github.com" className="ml-1 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
              View on GitHub
            </a>
          </p>
        </motion.footer>
      </div>
    </div>
  )
}
