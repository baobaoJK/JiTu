export const formatFileSize = (size: number) => {
  if (size < 1024) return size + ' B'
  const units = ['KB', 'MB', 'GB', 'TB']
  let i = -1
  do {
    size /= 1024
    i++
  } while (size >= 1024 && i < units.length - 1)
  return size.toFixed(2) + ' ' + units[i]
}
