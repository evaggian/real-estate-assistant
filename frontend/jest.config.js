module.exports = {
  testEnvironment: 'jsdom',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'script.js',
    '!node_modules/**'
  ],
  testMatch: [
    '**/test_script.test.js'
  ]
};
