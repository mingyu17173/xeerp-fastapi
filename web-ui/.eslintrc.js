module.exports = {
    root: true,
    parserOptions: {
        parser: '@babel/eslint-parser'
    },
    env: {
        browser: true,
        node: true,
        es6: true
    },
    extends: ['plugin:vue/recommended', 'eslint:recommended'],
    rules: {
        'vue/max-attributes-per-line': [2, {
            'singleline': 10,
            'multiline': {
                'max': 1
            }
        }],
        'indent': [2, 2, {
            'SwitchCase': 1
        }],
        'no-console': 'off',
    }
}
