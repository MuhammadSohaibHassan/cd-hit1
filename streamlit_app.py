import streamlit as st

def sequence_identity(seq1, seq2):
    """Calculate the sequence identity between two sequences."""
    if not seq1 or not seq2:
        return 0.0

    min_length = min(len(seq1), len(seq2))
    matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
    
    return matches / min_length

def cluster_sequences(sequences, identity_threshold):
    """Cluster sequences based on the specified identity threshold."""
    clusters = []
    
    for seq_id, seq in sequences.items():
        found_cluster = False

        for cluster in clusters:
            representative_seq = cluster[0][1]  # Get the sequence from the first item in the cluster
            if sequence_identity(seq, representative_seq) >= identity_threshold:
                cluster.append((seq_id, seq))  # Add the sequence ID and seq to the existing cluster
                found_cluster = True
                break

        if not found_cluster:
            clusters.append([(seq_id, seq)])  # Store as a tuple (seq_id, seq)
    
    return clusters

def read_fasta(uploaded_file):
    """Read sequences from a FASTA or text file."""
    sequences = {}
    seq_id = None
    seq = []

    # Read the uploaded file as text
    for line in uploaded_file:
        line = line.decode('utf-8').strip()  # Decode bytes to string and strip whitespace
        if line.startswith('>'):
            if seq_id is not None:
                sequences[seq_id] = ''.join(seq)
            seq_id = line[1:]  # Remove the '>'
            seq = []
        else:
            seq.append(line)

    # Save the last sequence if it exists
    if seq_id is not None:
        sequences[seq_id] = ''.join(seq)

    return sequences

def main():
    st.title("🧬 Sequence Clustering App")
    st.markdown("""
        Upload a FASTA or text file containing DNA or protein sequences. 
        The app will cluster the sequences based on the selected identity threshold.
    """)

    # File uploader for FASTA or text files
    uploaded_file = st.file_uploader("Upload a FASTA or text file", type=["fasta", "fa", "txt"])
    identity_threshold = st.slider("Select Identity Threshold", 0.0, 1.0, 0.9)

    if uploaded_file is not None:
        st.markdown("### Processing Sequences...")
        sequences = read_fasta(uploaded_file)

        if sequences:
            clusters = cluster_sequences(sequences, identity_threshold)
            st.write(f"**Total Sequences:** {len(sequences)}")
            st.write(f"**Total Clusters Found:** {len(clusters)}")

            for i, cluster in enumerate(clusters):
                st.write(f"### Cluster {i + 1}:")
                cluster_ids = [seq_id for seq_id, _ in cluster]  # Get only sequence IDs
                st.write(" - " + ", ".join(cluster_ids))  # Display only sequence IDs
        else:
            st.warning("No sequences found in the uploaded file.")

if __name__ == "__main__":
    main()
