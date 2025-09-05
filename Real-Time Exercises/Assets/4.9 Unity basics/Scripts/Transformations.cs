using UnityEngine;

public class Transformations : MonoBehaviour
{
    CreateGrid createGrid;

    Vector3[] startPos;

    [Header("Movement Controls")]
    public float moveFrequency = 2f;
    public float moveAmplitude = 5f;
    public float moveOffset = 0f;

    Vector3 startScale = Vector3.zero;

    [Header("Scale Controls")]
    public float scaleFrequency = 2f;
    public float scaleAmplitude = 5f;
    public float scaleOffset = 0f;

    [Header("Rotation Controls")]
    public float rotationSpeed = 1f;

    private void Start()
    {
        createGrid = GetComponent<CreateGrid>();
        startPos = createGrid.startPos;
        startScale = createGrid.grid[0].localScale;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
