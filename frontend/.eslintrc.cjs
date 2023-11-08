module.exports = {
    "env": {
        "browser": true,
        "es2021": true
    },
    "ignorePatterns": [
        'vite.config.ts',
        '.eslintrc.cjs'
    ],
    "extends": [
        "standard-with-typescript",
        "plugin:react/recommended"
    ],
    "overrides": [
        {
            "env": {
                "node": true
            },
            "files": [
                ".eslintrc.{js,cjs}"
            ],
            "parserOptions": {
                "sourceType": "script"
            }
        }
    ],
    "parserOptions": {
        "ecmaVersion": "latest",
        "sourceType": "module"
    },
    "plugins": [
        "react"
    ],
    "rules": {
        "semi": [
            "error",
            "always"
        ],
        "@typescript-eslint/semi": [
            "error",
            "always",
        ],
        "no-extra-semi": "off"
    }
}
