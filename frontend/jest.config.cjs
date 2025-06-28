module.exports = {
    transform: {
        "^.+\\.(ts|tsx|js|jsx)$": "babel-jest",
    },
    testEnvironment: "jest-environment-jsdom",
    moduleFileExtensions: ["js", "jsx", "ts", "tsx", "json", "node"],
    moduleNameMapper: {
        "\\.(css|less|scss|sass)$": "identity-obj-proxy",
        "\\.(svg|png|jpg|jpeg|gif|webp|avif|ico|bmp|tiff)$":
            "<rootDir>/__mocks__/fileMock.js",
    },
    setupFilesAfterEnv: ["<rootDir>/src/setupTests.js"],
};
