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
        
        # Update the progress bar
        progress_bar = st.progress(0)
        
        for i, cluster in enumerate(clusters):
            representative_seq = cluster[0]
            if sequence_identity(seq, representative_seq) >= identity_threshold:
                cluster.append(seq)  # Add to the existing cluster
                found_cluster = True
                break
            
            # Update progress bar
            progress_bar.progress((i + 1) / len(clusters))

        if not found_cluster:
            clusters.append([seq])
        
        # Update progress bar for the remaining sequences
        progress_bar.progress(1.0)  # Complete progress

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
                for seq in cluster:
                    match_percentage = sequence_identity(cluster[0], seq) * 100  # Calculate match percentage
                    st.write(f" - `{seq[:50]}...` (Match: **{match_percentage:.2f}%**)")  # Display first 50 chars and match percentage
        else:
            st.warning("No sequences found in the uploaded file.")

if __name__ == "__main__":
    main()
