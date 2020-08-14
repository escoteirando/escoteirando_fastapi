const local_storage_factory = () => {
    const setValue = (key, value, validUntil = 0) => {
        const v = { _v: value, _u: validUntil }
        localStorage.setItem(key, JSON.stringify(v))
    }

    const getValue = (key, defaultValue = null) => {
        let v = localStorage.getItem(key)
        if (v) {
            try {
                v = JSON.parse(v)
                if (v._u <= 0 || v._u > currentTimeStamp()) {
                    if (v._v) { defaultValue = v._v }
                }
            } catch (e) {
                console.error('[LOCALSTORAGE] Error on getValue', key, e)
            }
        }
        return defaultValue
    }

    const deleteValue = (key) => localStorage.removeItem(key)

    return {
        setValue,
        getValue,
        deleteValue
    }
}

const currentTimeStamp = () => Math.round((new Date()).getTime() / 1000)

export { local_storage_factory, currentTimeStamp }
