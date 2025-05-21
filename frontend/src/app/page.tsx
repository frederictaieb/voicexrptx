'use client'
import { useEffect, useState } from 'react'

type Item = {
  id: number
  name: string
}

export default function Home() {
  const [items, setItems] = useState<Item[]>([])

  useEffect(() => {
    const fetchItems = async () => {
      const response = await fetch('http://localhost:8000/api/items')
      const data = await response.json()
      setItems(data)
    }

    fetchItems()
  }, [])

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Liste des Items depuis FastAPI</h1>
      <ul>
        {items.map((item: Item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </main>
  )
}
